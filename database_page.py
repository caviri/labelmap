import streamlit as st
import pandas as pd
import io
import json

@st.cache
def parsejson(string_data):
    di = json.loads(string_data)

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
            'url_ref': di['url_ref']}
            # 'image_url': url_image,
            # 'image_files': ioimages,
            # 'audio_url': url_audio,
            # 'audio_files': ioaudio,
            # 'video_url': url_video,
            # 'video_files': iovideo}

    return pd.DataFrame(df_dicts,index = [0])

st.set_page_config(page_title="Labelmap test", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown("# Labelmap list")
st.sidebar.markdown("# Labelmap list")

dbfile = st.file_uploader("Choose files", accept_multiple_files=True)

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
    'url_ref': []}

df = pd.DataFrame(df_dicts)

if len(dbfile) > 0:
    for file in dbfile:
        # To convert to a string based IO:
        stringio = io.StringIO(file.getvalue().decode("utf-8"))
        string_data = stringio.read()

        dft = parsejson(string_data)
        df = pd.concat([df,dft])

# else:
#     df_dicts = {
#         'title': [], 
#         'date': [],
#         'author': [],
#         'original_author': [],
#         'language': [],
#         'score': [],
#         'kids': [],
#         'robot': [],
#         'categories': [],
#         'playlist': [],
#         'playlist_position': [],
#         'address': [],
#         'coordinates': [],
#         'license': [],
#         'reference': [],
#         'url_ref': []}

#     df = pd.DataFrame(df_dicts)



st.dataframe(df)
