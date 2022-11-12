import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import datetime
import json

import io
import base64
from PIL import Image

st.set_page_config(page_title="Labelmap test", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown("# Labelmap test")
st.sidebar.markdown("# Labelmap test")

previousfile = st.sidebar.file_uploader("Choose a file")
if previousfile is not None:
    stringio = io.StringIO(previousfile.getvalue().decode("utf-8"))

    string_data = stringio.read()
    di = json.loads(string_data)
    st.sidebar.json(di['map']['center'])

    lat = di['map']['center']['lat']
    lng = di['map']['center']['lng']

else:
    lat = 37.017654
    lng = -4.568592



c1, c2 = st.columns([3,1])

# Title
title = c1.text_input('Title', 'Title of the item')

with c1:
    st.write('Title saved: ', title)

# Text area
txt = c1.text_area('Text to analyze', 'Introduce here the transcription', height=500)


## Map
m = folium.Map(location=[lat, lng], zoom_start=7,
                attr='ESRI',
                name='satellite',
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")

Draw(export=True).add_to(m)

folium.TileLayer('openstreetmap').add_to(m)
folium.LayerControl().add_to(m)

with c1:
    output = st_folium(m, width=700, height=500)


### c2

# Dateselect
d = c2.date_input("Introduce date", datetime.datetime.now())

au = c2.selectbox('Author?', ('Alejandro', 'Carlos', 'Manuel', 'Luis'))

l = c2.text_input("Language", "Introduce language")

# Multiselect
options = c2.multiselect(
    'Categories',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

pl = c2.text_input("Playlist", "Playlist title")

plp = c2.text_input("Playlist position", "Playlist position")

add = c2.text_input("Address", "Introduce addresss")

coor = c2.text_input("Address", "Introduce Coordinates")

license = c2.text_input("License", "Introduce License")

reference = c2.text_input("License", "Introduce Reference")

url = c2.text_input("URL", "Introduce url")


### Upload 
c3, c4, c5 = st.columns(3)

up_images = c3.file_uploader("Update images files", accept_multiple_files=True)

up_audio = c4.file_uploader("Update audio files", accept_multiple_files=True)

up_video = c5.file_uploader("Update video files", accept_multiple_files=True)

for uploaded_file in up_images:
    stringio = base64.b64encode(uploaded_file.getvalue()).decode()
    st.write("filename:", uploaded_file.name)

if len(up_images) == 0:
    ioimages = 'None'

if len(up_audio) == 0:
    ioaudio = 'None'

if len(up_video) == 0:
    iovideo = 'None'

## Download
@st.cache
def createJSON():
    dicts = {'title': title, 'options': options, 'map': output, 'images': ioimages, 'audios': ioaudio, 'videos': iovideo}
    js = json.dumps(dicts)
    return js

js = createJSON()
st.download_button(
    label="Download data as JSON",
    data=js,
    file_name='data.json',
    mime='text/json',
)