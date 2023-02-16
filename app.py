import streamlit as st
from streamlit_option_menu import option_menu
import os
import re
import string
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import seaborn as sns
bersihdata = " "
csv_data = pd.read_csv("data.csv", encoding = 'ISO-8859-1')
df_kamusalay = pd.read_csv("new_kamusalay.csv", encoding = 'ISO-8859-1', header=None,index_col=0,squeeze=True)
dict_kamusalay = df_kamusalay.to_dict()
df_stopwords = pd.read_csv("abusive.csv", encoding = 'ISO-8859-1')
list_stopwords = df_stopwords["ABUSIVE"].tolist()
with st.sidebar:
    selected = option_menu ("MENU",["Form Text","Form CSV"])
def emoticon (data):
    data = re.sub(r'\\x[0-9A-Fa-f]{2}', '', data)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', data)
        
def lowercase (data):
    data = data.lower()
    return data
def replaceThreeOrMore (data):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    data = pattern.sub(r"\1", data)
    return data
def stemming (data) :
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data = stemmer.stem(data)
    return data
def tokenization (data) :
    data = data.split()
    return data
def normalization (data) :
    for i in data :
        for key, value in dict_kamusalay.items():
            if key not in data:
                continue
            index = data.index(key)
            data[index] = value
    return data
def number (data):
    data = str(data)
    data = re.sub(r'\d+','',data)
    data = data.split() 
    return data
def punctuation (data) :
    data = str(data)
    data = re.sub('-', ' ', data)
    data = re.sub(r'[^\w\s]', ' ', data)
    data = data.split()
    return data
def stopwords (data) :
    for i in reversed (data) :
        if i in list_stopwords :
            data.remove(i)
    return data
def to_string (data) :
    data = ' '.join(map(str,data))
    return data
def update_csv (uploadedfile):
    with open (os.path.join("data.csv"),"wb") as f:
        f.write (uploadedfile.getbuffer())
        return st.success ("Saved file:{} ".format(uploadedfile.name))
st.title ("FORM")
if selected == "Form Text":
    st.subheader ("Input :")
    bersihdata = st.text_area ("Input :",bersihdata, height = 150)
    running_cleansing_text = st.button ("Proses")
        
    if running_cleansing_text:
        bersihdata = emoticon (bersihdata)
        bersihdata = lowercase (bersihdata)
        bersihdata = replaceThreeOrMore (bersihdata)
        bersihdata = stemming (bersihdata)
        bersihdata = tokenization (bersihdata)
        bersihdata = normalization (bersihdata)
        bersihdata = number (bersihdata)
        bersihdata = punctuation (bersihdata)
        bersihdata = stopwords (bersihdata)
        bersihdata = to_string (bersihdata)

    st.subheader ("Output :")
    st.text_area ("Output :", value = bersihdata, height  = 150)


if selected == "Form CSV":
    st.subheader ("Input :")
    upload_file1 = st.file_uploader ("Input CSV")
    if upload_file1 is not None :
        csvupload = pd.read_csv(upload_file1, encoding = 'ISO-8859-1')
        st.dataframe (csvupload)
    clicked = st.button ("Proses Upload")
    if clicked :
        update_csv (upload_file1)
        csv_data = csvupload
        st.subheader ("File CSV Upload")
        st.dataframe (csv_data)
    st.subheader ("Baris :")
    pilih_baris = st.text_input ("Baris :", value = "Tweet", label_visibility="collapsed" )
    st.subheader ("Kolom:")
    pilih_kolom = st.number_input ("Kolom ke :", value = 1, key = int, step = 1, min_value=None, max_value=None, label_visibility="collapsed" )
    bersihdata = csv_data[pilih_baris][pilih_kolom]        
    st.subheader ("Input Text :")
    st.text_area ("Input Text :", value = bersihdata, height =150, label_visibility ="collapsed" )
    clean_2 = st.button ("Prosess")
    if clean_2:
        bersihdata = emoticon (bersihdata)
        bersihdata = lowercase (bersihdata)
        bersihdata = replaceThreeOrMore (bersihdata)
        bersihdata = stemming (bersihdata)
        bersihdata = tokenization (bersihdata)
        bersihdata = normalization (bersihdata)
        bersihdata = number (bersihdata)
        bersihdata = punctuation (bersihdata)
        bersihdata = stopwords (bersihdata)
        bersihdata = to_string (bersihdata)
    st.subheader ("Output :")
    st.text_area ("Output :", value = bersihdata, height = 200,label_visibility="collapsed")