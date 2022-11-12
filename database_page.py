import streamlit as st
import pandas as pd
import io
import json

st.set_page_config(page_title="Labelmap test", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
st.markdown("# Labelmap test")
st.sidebar.markdown("# Labelmap test")

dbfile = st.file_uploader("Choose a file")
if dbfile is not None:
    # To convert to a string based IO:
    stringio = io.StringIO(dbfile.getvalue().decode("utf-8"))
    #st.sidebar.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    di = json.loads(string_data)

    lat = di['map']['center']['lat']
    lng = di['map']['center']['lng']
    dft = pd.DataFrame({'title':[lat],'value':[lng]})

    df = pd.concat([df,dft])
else:
    df = pd.DataFrame({'title':[],'value':[]})
    
st.dataframe(df)
