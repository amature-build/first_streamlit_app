import streamlit as st
import pandas as pd
import requests as r

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

fruityvice_response = r.get(r"https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
