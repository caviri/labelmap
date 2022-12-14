import streamlit as st
import pandas as pd
import io
import json
import datetime

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode

import folium
from folium.plugins import Draw

from streamlit_folium import st_folium
import numpy as np

import base64
from PIL import Image
from geopy.geocoders import Nominatim

from unidecode import unidecode

@st.cache
def parsejson(di):

    df_dicts = {
            'title': di['title'],
            'date': di['date'],
            'author': di['author'],
            'original_author': di['original_author'],
            'language': di['language'],
            'score': di['score'],
            'kids': di['kids'],
            'robot': di['robot'],
            'categories': di['categories'],
            'playlist': di['playlist'],
            'playlist_position': di['playlist_position'],
            'address': di['address'],
            'coordinates': di['coordinates'],
            'license': di['license'],
            'reference': di['reference'],
            'url_ref': di['url_ref'],
            'image_url': di['image_url'],
            'time_duration': str(datetime.datetime.strptime(di['log']['export_dt'], "%Y/%m/%d_%H:%M:%S")-datetime.datetime.strptime(di['log']['init_dt'],"%Y/%m/%d_%H:%M:%S" ))}
            # 'image_files': ioimages,
            # 'audio_url': url_audio,
            # 'audio_files': ioaudio,
            # 'video_url': url_video,
            # 'video_files': iovideo}
    return pd.DataFrame(df_dicts,index = [0])

st.set_page_config(page_title="Labelmap test", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown("# Labelmap list")
st.write('Drag and drop your json files and select one item from the table.')
st.sidebar.markdown("# Labelmap list")

dbfile = st.sidebar.file_uploader("Choose files", accept_multiple_files=True)

df_dicts = {
    'title': [],
    'date': [],
    'author': [],
    'original_author': [],
    'language': [],
    'score': [],
    'kids': [],
    'robot': [],
    'categories': [],
    'playlist': [],
    'playlist_position': [],
    'address': [],
    'coordinates': [],
    'license': [],
    'reference': [],
    'url_ref': [],
    'image_url': [],
    'time_duration': []}

df_table = pd.DataFrame(df_dicts)
di_list = []

if len(dbfile) > 0:
    for file in dbfile:
        # To convert to a string based IO:
        stringio = io.StringIO(file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        di = json.loads(string_data)
        di_list.append(di)
        dft = parsejson(di)
        df_table = pd.concat([df_table,dft])



#st.dataframe(df)

#https://discuss.streamlit.io/t/display-images-in-aggrid-table/18434/8
ShowImage = JsCode("""function (params) {
            var element = document.createElement("span");
            var imageElement = document.createElement("img");
        
            if (params.data.image_url != '') {
                imageElement.src = params.data.image_url;
                imageElement.width="50";
            } else { imageElement.src = ""; }
            element.appendChild(imageElement);
            element.appendChild(document.createTextNode(params.value));
            return element;
            }""")


df_table['images'] = ''

df_table.insert(0, 'images', df_table.pop('images'))

gd = GridOptionsBuilder.from_dataframe(df_table)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, filter=True, sortable=True)
gd.configure_column('images', cellRenderer=ShowImage)
#sel_mode = st.sidebar.radio("Selection Type", options= ["single", "multiple"], index=0)
gd.configure_selection(use_checkbox=False, selection_mode="single")
gridoptions = gd.build()
grid_table = AgGrid(df_table, gridOptions=gridoptions, 
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    height=300,
                    allow_unsafe_jscode=True,
                    theme="streamlit")


sel_row = grid_table["selected_rows"]

st.markdown("""---""")

#st.write(sel_row)

if len(sel_row) > 0:
    di = di_list[sel_row[0]['_selectedRowNodeInfo']['nodeRowIndex']]

    title = di['title']
    txt = di['transcription']
    d = datetime.datetime.strptime(di['date'], "%Y/%m/%d")

    authors = ('None','Alejandro', 'Carlos', 'Manuel', 'Luis')
    author_index = authors.index(di['author'])
    au = di['author']

    original_author = di['original_author']
    l = di['language']
    score = di['score']
    kids = di['kids']
    robot = di['robot']
    categories = di['categories']
    pl = di['playlist']
    plp = di['playlist_position']
    add = di['address']
    coor = di['coordinates']
    license = di['license']
    reference = di['reference']
    url_ref = di['url_ref']
    url_image = di['image_url']
    ioimages = di['image_files']
    url_audio = di['audio_url']
    ioaudio = di['audio_files']
    url_video = di['video_url']
    iovideo = di['video_files']
    folium_output = di['map']

    lat = di['map']['center']['lat']
    lng = di['map']['center']['lng']

else:
    title = ''
    txt = ''
    d = datetime.datetime.now()
    author_index = 0
    original_author = ''
    l = ''
    score = 0
    kids = False
    robot = False
    categories = ''
    pl = ''
    plp = ''
    add = ''
    coor = ''
    license = ''
    reference = ''
    url_ref = ''
    url_image = ''
    ioimages = None
    url_audio = ''
    ioaudio = None
    url_video = ''
    iovideo = None
    folium_output = None

    lat = 37.017654
    lng = -4.568592

def isSaved(output, ssection):
    if output:
        with ssection:
            st.write('⬆️🤗💚💚💚💚💚💚💚💚 Saved! 💚💚💚💚💚💚💚💚🤗⬆️')
    else:
        ssection.write('⬆️⚠️🚨🚨🚨🚨🚨🚨🚨🚨 Not saved! 🚨🚨🚨🚨🚨🚨🚨🚨⚠️⬆️')

######################## Streamlit app ########################
st.markdown(f'## Item preview')
left, right = st.columns([2,1])

left.markdown(f'### {title}')
left.write(add)
try:
    left.image(url_image)
except:
    pass
right.write(txt)


st.markdown("""---""")

######################## Streamlit app ########################

st.markdown('## Labelmap Editor')
c1, c2 = st.columns([3,1])

# Title
title = c1.text_input('Title', value=title, placeholder='Item title')
isSaved(title, c1)

# Text area
txt = c1.text_area('Transcription', value=txt, placeholder='Introduce here transcription', height=500)
isSaved(txt, c1)

## Map
def plot_map(lat, lng, coor, width=800, height=600):
    m = folium.Map(location=[lat, lng], zoom_start=8,
                    attr='ESRI',
                    name='satellite',
                    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")

    Draw(export=True).add_to(m)

    folium.TileLayer('openstreetmap').add_to(m)
    folium.LayerControl().add_to(m)

    try:
        latm = float(coor.split(',')[0])
        lngm = float(coor.split(',')[1])
        folium.Marker(location=[latm, lngm]).add_to(m)
    except Exception as e:
        #c1.write(e)
        pass

    
    output = st_folium(m, width=width, height=height)
    return output

with c1:
    #le, mi, ri = st.columns([1,1,1])
    coor = st.text_input("Coordinates", value=coor, placeholder="Introduce Coordinates")
    # width = st.text_input("Width", value=800)
    # height = st.text_input("Height", value=600)

    try:
        locator = Nominatim(user_agent="myRevGeocoder")
        location = locator.reverse(coor)
        address_nominatim = location.address
        st.write(address_nominatim)
    except Exception as e:
        #st.write(e)
        pass

    folium_output = plot_map(lat, lng, coor)

try: 
    latm = folium_output['all_drawings'][0]['geometry']['coordinates'][1]
    lngm = folium_output['all_drawings'][0]['geometry']['coordinates'][0]
    coor = str(latm) + ',' + str(lngm)
except Exception as e:
    #c1.write(e)
    pass


### c2
#####################################################
d = c2.date_input("Introduce date", value=d)

au = c2.selectbox('Author', ('None','Alejandro', 'Carlos', 'Manuel', 'Luis'), index=author_index)

original_author = c2.text_input('Original author', value=original_author, placeholder='Introduce original author of text')

isSaved(original_author, c2)

l = c2.text_input("Language", value=l, placeholder="Introduce language")

isSaved(l, c2)

score  = c2.slider('Quality', 0, 5, score)

kids = c2.checkbox('Kids', value=kids)

robot = c2.checkbox('Artificial Voice', value=robot)

# categories = c2.multiselect(
#     'Categories',
#     ['Green', 'Yellow', 'Red', 'Blue'],
#     ['Yellow', 'Red'])

categories = c2.text_input('Categories', value=categories, placeholder='Introduce categories separated by semi-colon ;')

isSaved(categories, c2)

pl = c2.text_input("Playlist", value=pl, placeholder="Playlist title")
isSaved(pl, c2)
plp = c2.text_input("Playlist position (Integer)", value=plp, placeholder="Playlist position")
isSaved(plp, c2)

add = c2.text_input("Address", value=add, placeholder="Introduce address")
isSaved(add, c2)
# coor = c2.text_input("Coordinates", value=coor, placeholder="Introduce Coordinates")
# isSaved(coor, c2)

try:
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(add)
    c2.write(f'{location.latitude}, {location.longitude}')
except Exception as e:
    #st.write(e)
    pass

license = c2.text_input("License", value=license, placeholder="Introduce License")
isSaved(license, c2)
reference = c2.text_input("Reference", value=reference, placeholder="Introduce Reference")
isSaved(reference, c2)

url_ref = c2.text_input("Reference URL", value=url_ref, placeholder="Introduce reference URL")
isSaved(url_ref, c2)


### Upload 
################################################
c3, c4, c5 = st.columns(3)

url_image = c3.text_input("Image URL (Optional)", value=url_image, placeholder="Introduce image url")
isSaved(url_image, c3)
up_images = c3.file_uploader("Update images files", accept_multiple_files=True)

url_audio = c4.text_input("Audio URL (Optional)", value=url_audio, placeholder="Introduce audio url")
isSaved(url_audio, c4)
up_audio = c4.file_uploader("Update audio files", accept_multiple_files=True)

url_video = c5.text_input("Video URL (Optional)", value=url_video, placeholder="Introduce video url")
isSaved(url_video, c5)
up_video = c5.file_uploader("Update video files", accept_multiple_files=True)

if len(up_images) == 0:
    ioimages = []
elif ioimages:
    for uploaded_file in up_images:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        ioimages.append(stringio)
else:
    ioimages = []
    for uploaded_file in up_images:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        ioimages.append(stringio)

if len(up_audio) == 0:
    ioaudio = []
elif ioaudio:
    for uploaded_file in up_audio:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        ioaudio.append(stringio)
else:
    ioaudio = []
    for uploaded_file in up_audio:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        ioaudio.append(stringio)

if len(up_video) == 0:
    iovideo = []
elif iovideo:
    for uploaded_file in up_video:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        iovideo.append(stringio)
else:
    iovideo = []
    for uploaded_file in up_video:
        stringio = base64.b64encode(uploaded_file.getvalue()).decode()
        iovideo.append(stringio)

c3.markdown(str(len(ioimages)) + ' images uploaded')
c4.markdown(str(len(ioaudio)) + ' audios uploaded')
c5.markdown(str(len(iovideo)) + ' videos uploaded')


### Initial DT
@st.experimental_singleton
def get_initdt():
    return datetime.datetime.now()

initdt = get_initdt()

## Download
@st.cache
def createJSON():

    exportdt = datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S")

    dicts = {
            'title': title, 
            'transcription': txt,
            'date': d.strftime("%Y/%m/%d"),
            'author': au,
            'original_author': original_author,
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

            'log': {
                'version_labelmap': '0.4',
                'init_dt': initdt.strftime("%Y/%m/%d_%H:%M:%S"),
                'export_dt': exportdt,
                }
            }

    js = json.dumps(dicts)
    return js

@st.cache
def get_export_filename():

    if len(title) > 0:
        exportdt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        exportti = title.split(' ')
        if len(exportti) > 1:
            export_filename = exportdt + '_' + exportti[0] + '_' + exportti[1] + '.json'
        else:
            export_filename = exportdt + '_' + exportti[0] + '.json'
    else:
        export_filename = 'export.json'

    return unidecode(export_filename)



# js = createJSON()
 
st.download_button(
    label="Download data as JSON",
    data=createJSON(),
    file_name=get_export_filename(),
    mime='text/json',
)