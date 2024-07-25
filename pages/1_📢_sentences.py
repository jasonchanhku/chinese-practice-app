import streamlit as st
#import streamlit.components.v1 as components
import random
import pandas
from utils import chinese_sentences
import base64

# -------------- app config ---------------
#st.set_page_config(page_title="Chinese Words Practice", page_icon="🗨️")

# ---------------- functions ----------------
# external css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def select_callback():
    st.session_state.selected_state = True
    #st.session_state.word_number = int(specific_word) - 1
# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.write("**Author: Jason Chan**")
    st.markdown("""
    
    # Exam Format
    
    - Read out 10 sentences
    """)
# ---------------- CSS ----------------

local_css("style.css")

number_sentences = len(chinese_sentences)
st.caption("Currently we have " + str(number_sentences) + " words in the database")


specific_chapter = st.selectbox("Select specific chapter",
                                [None, 1, 2, 3, 4], label_visibility="collapsed", index=None, on_change=select_callback)

if specific_chapter is not None:
    chinese_sentences = list(filter(lambda sentence: sentence.chapter == specific_chapter, chinese_sentences))    
    st.markdown(f"<h4 style='text-align: center;'>Chapter {specific_chapter} </h4>", unsafe_allow_html=True)
else:
    st.markdown(f"<h4 style='text-align: center;'> All Chapters </h4>", unsafe_allow_html=True)

for sentence in chinese_sentences:
    st.text(f"PY: {sentence.pinyin}\nCH: {sentence.sentences}\nEN: {sentence.translation}")
    st.audio(base64.b64decode(sentence.pronounciation_audio_bytes.encode('utf-8')))
    st.divider()
        
st.markdown(
    '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
    unsafe_allow_html=True,
)
