import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import datetime

st.set_page_config(page_title="Labelmap test", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown("# Labelmap test")
st.sidebar.markdown("# Labelmap test")

# Dataframe
df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20)))

st.dataframe(df)


# Dateselect
d = st.date_input(
    "When's your birthday",
    datetime.date(2019, 7, 6))
st.write('Your birthday is:', d)


# Multiselect
options = st.multiselect(
    'What are your favorite colors',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('You selected:', options)

# Text area
txt = st.text_area('Text to analyze', '''
    It was the best of times, it was the worst of times, it was
    the age of wisdom, it was the age of foolishness, it was
    the epoch of belief, it was the epoch of incredulity, it
    was the season of Light, it was the season of Darkness, it
    was the spring of hope, it was the winter of despair, (...)
    ''')

# Map
m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)
Draw(export=True).add_to(m)

c1, c2 = st.columns(2)
with c1:
    output = st_folium(m, width=700, height=500)

with c2:
    st.json(output)


# Upload multiples files
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

## Single file uploader
# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)