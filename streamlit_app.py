import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import datetime
import json

import io

st.set_page_config(page_title="Labelmap test", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown("# Labelmap test")
st.sidebar.markdown("# Labelmap test")

previousfile = st.sidebar.file_uploader("Choose a file")
if previousfile is not None:
    # # To read file as bytes:
    # bytes_data = previousfile.getvalue()
    # st.sidebar.write(bytes_data)

    # To convert to a string based IO:
    stringio = io.StringIO(previousfile.getvalue().decode("utf-8"))
    #st.sidebar.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    di = json.loads(string_data)
    st.sidebar.json(di['map']['center'])

    lat = di['map']['center']['lat']
    lng = di['map']['center']['lng']
    # # Can be used wherever a "file-like" object is accepted:
    # dataframe = pd.read_csv(uploaded_file)
    # st.sidebar.write(dataframe)
else:
    lat = 37.017654
    lng = -4.568592

# Dataframe
df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20)))

st.dataframe(df)

# Title
title = st.text_input('Title', 'Life of Brian')
st.write('The current movie title is', title)

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
txt = st.text_area('Text to analyze', '''It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, (...) ''', height=500)

st.write('Your birthday is:', txt)
# Map

c1, c2 = st.columns(2)

# if st.sidebar.checkbox('Reload map'):
#     m = folium.Map(location=[lat, lng], zoom_start=5)
#     Draw(export=True).add_to(m)

#     with c1:
#         output = st_folium(m, width=700, height=500)

#     with c2:
#         st.json(output)
            
# else:
#     output = json.dumps({'test':1})

m = folium.Map(location=[lat, lng], zoom_start=5,
                attr='ESRI',
                name='satellite',
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")

Draw(export=True).add_to(m)

folium.TileLayer('openstreetmap').add_to(m)
folium.LayerControl().add_to(m)

with c1:
    output = st_folium(m, width=700, height=500)

# with c2:
#     st.json(output)

import base64

# Upload multiples files
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    #bytes_data = uploaded_file.read()
    #stringio = StringIO(uploaded_file.getvalue().decode("base64")).read()
    stringio = base64.b64encode(uploaded_file.getvalue()).decode()
    st.write("filename:", uploaded_file.name)

from PIL import Image

if len(uploaded_files) == 0:
    stringio = 'None'
else:
    # img = Image.open(io.BytesIO(base64.b64decode(stringio)))
    # st.image(img)
    st.video(io.BytesIO(base64.b64decode(stringio)))

    
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

## Download
@st.cache
def createJSON():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #mapinfo = json.loads(output)
    dicts = {'title': title, 'options': options, 'map': output, 'file': stringio}
    js = json.dumps(dicts)
    return js



js = createJSON()
st.download_button(
    label="Download data as JSON",
    data=js,
    file_name='data.json',
    mime='text/json',
)