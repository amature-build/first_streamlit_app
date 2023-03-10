import streamlit as st
import pandas as pd
import requests as r
import snowflake.connector as scon
from urllib.error  import URLError

def get_fruityvice_data(new_fruit_choice):
  fruityvice_response = r.get(r"https://fruityvice.com/api/fruit/" + new_fruit_choice)
  # take the json response and normalize it
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# extract list from snowflake
def get_fruit_load_list():
  with scon.connect(**st.secrets["snowflake"]) as con:
    cur = con.cursor()
    cur.execute("select * from fruit_load_list")
    return cur.fetchall()
  
#  insert data into fruit_load_list table in snowflake
def insert_row_snowflake(new_fruit):
  with scon.connect(**st.secrets['snowflake']) as con:
    cur = con.cursor()
    cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

st.title('My Mom\'s New Healthy Diner')

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Read data with pandas read_csv
my_fruit_list = pd.read_csv(r"https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set the index base on column name Fruit
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple', 'Avocado'])

fruit_to_show = my_fruit_list.loc[fruit_selected]

# Display the table on the page.
st.dataframe(fruit_to_show)

# New Section to disply fruityvice api responce
st.header('Fruityvice Fruit Advice!')

fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)

fruityvice_normalized = get_fruityvice_data(fruit_choice)

# output it as table
st.dataframe(fruityvice_normalized)

st.header('View Our Fruit List - Add Your Favorites!')
if st.button('Get Fruit List'):
  sf_data = get_fruit_load_list()
  st.dataframe(sf_data)

add_fruit = st.text_input(r'What fruit would you like to add?', 'Jackfruit')
if st.button('Add a Fruit to the List'):
  add_fruit_output = insert_row_snowflake(add_fruit)
  st.text(add_fruit_output)
