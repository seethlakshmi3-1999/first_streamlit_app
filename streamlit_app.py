import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥠Omega 3 & Blueberry Oatmeal')
streamlit.text('🌮Kale, Spinach & Rocket Smoothie')
streamlit.text('🥯🌭Hard-Boiled Free-Range Egg')
streamlit.text('🥝Avacado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
#streamlit.dataframe(my_fruit_list)
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)
streamlit.header("fruityvice fruit advice!")
try:
  fruit_choice=streamlit.text_input("what fruit would you like information about?",'kiwi')
  if not fruit_choice:
      streamlit.write('the user entered',fruit_choice)
  else:
      fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
      fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)
except URLError as e:
      streamlit.error()
#import snpwflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_rows)


add_my_fruit=streamlit.text_input("what fruit would you like information about?","Jackfruit")
streamlit.write('Thanks for adding',add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
