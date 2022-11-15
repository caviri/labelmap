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

st.sidebar.image('img/TMMlogo.png', width=150)

st.sidebar.markdown("""# Load previous session

This is useful to recover previous values and avoid having to re-enter them. For instance, when introducing items from the same playlist or close locations. 

Do not forget in this case to erase the previous files. 

""")

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




######################## Streamlit app ########################
c1, c2 = st.columns([3,1])

# Title
title = c1.text_input('Title', placeholder='Item title')

# with c1:
#     st.write('Title saved: ', title)

# Text area
txt = c1.text_area('Text to analyze', placeholder='Introduce here transcription', height=500)


## Map
m = folium.Map(location=[lat, lng], zoom_start=7,
                attr='ESRI',
                name='satellite',
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")

Draw(export=True).add_to(m)

folium.TileLayer('openstreetmap').add_to(m)
folium.LayerControl().add_to(m)

with c1:
    folium_output = st_folium(m, width=700, height=500)


### c2
#####################################################
d = c2.date_input("Introduce date", datetime.datetime.now())

au = c2.selectbox('Author', ('Alejandro', 'Carlos', 'Manuel', 'Luis'))

l = c2.text_input("Language", placeholder="Introduce language")

score  = c2.slider('Quality', 0, 5, 1)

kids = c2.checkbox('Kids', value=False)

robot = c2.checkbox('Artificial Voice', value=False)

categories = c2.multiselect(
    'Categories',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

pl = c2.text_input("Playlist", placeholder="Playlist title")
plp = c2.text_input("Playlist position (Integer)", placeholder="Playlist position")

add = c2.text_input("Address", placeholder="Introduce address")
coor = c2.text_input("Address", placeholder="Introduce Coordinates")

license = c2.text_input("License", placeholder="Introduce License")
reference = c2.text_input("Reference", placeholder="Introduce Reference")

url_ref = c2.text_input("Reference URL", placeholder="Introduce reference URL")


### Upload 
################################################
c3, c4, c5 = st.columns(3)

url_image = c3.text_input("Image URL (Optional)", placeholder="Introduce image url")
up_images = c3.file_uploader("Update images files", accept_multiple_files=True)

url_audio = c4.text_input("Audio URL (Optional)", placeholder="Introduce audio url")
up_audio = c4.file_uploader("Update audio files", accept_multiple_files=True)

url_video = c5.text_input("Video URL (Optional)", placeholder="Introduce video url")
up_video = c5.file_uploader("Update video files", accept_multiple_files=True)

if len(up_images) == 0:
    ioimages = 'None'
else:
    ioimages = []
    for uploaded_file in up_images:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        ioimages.append(stringio)

if len(up_audio) == 0:
    ioaudio = 'None'
else:
    ioaudio = []
    for uploaded_file in up_audio:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        ioaudio.append(stringio)

if len(up_video) == 0:
    iovideo = 'None'
else:
    iovideo = []
    for uploaded_file in up_video:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        iovideo.append(stringio)

## Download
@st.cache
def createJSON():
    dicts = {
            'title': title, 
            'transcription': txt,
            'date': d.strftime("%Y-%m-%d"),
            'author': au,
            'language': l,
            'score': score,
            'kids': kids,
            'robot': robot,
            'categories': categories,
            'playlist': pl,
            'playlist_position': plp,
            'address': add,
            'coordinates': coor,
            'license': license,
            'reference': reference,
            'url_ref': url_ref,
            'image_url': url_image,
            'image_files': ioimages,
            'audio_url': url_audio,
            'audio_files': ioaudio,
            'video_url': url_video,
            'video_files': iovideo,
            'map': folium_output, 
            }


    js = json.dumps(dicts)
    return js

js = createJSON()
st.download_button(
    label="Download data as JSON",
    data=js,
    file_name='data.json',
    mime='text/json',
)