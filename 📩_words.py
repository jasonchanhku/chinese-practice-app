import streamlit as st
#import streamlit.components.v1 as components
import random
import pandas
from utils import chinese_keywords, chinese_keywords_df
import base64

# -------------- app config ---------------
st.set_page_config(page_title="Chinese Words Practice", page_icon="🗨️")

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
# ---------------- CSS ----------------

local_css("style.css")

# ---------------- SESSION STATE ----------------
    
if "word_number" not in st.session_state:
    st.session_state.word_number = 0

if "selected_state" not in st.session_state:
    st.session_state.selected_state = False
# ---------------- Main page ----------------

tab1, tab2 = st.tabs(["Flashcards", "Search engine"])

# rows = pandas.read_csv("./data/chinese_keywords_sample.csv")

word_list = [i for i in range(1, len(chinese_keywords)+1)]

with tab1:
    # st.title("Product Owner Interview words Flashcards")
    number_words = len(chinese_keywords)
    st.caption("Currently we have " + str(number_words) + " words in the database")

    # ---------------- words & answers logic ----------------

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        previous_word = st.button(
            "Previous word", key="Previous", use_container_width=True
        )

    with col2:
        next_word = st.button(
            "Next word", key="Next", use_container_width=True
        )

    with col3:
        specific_word = st.selectbox("Select specific word",
                                     word_list, label_visibility="collapsed", index=None, on_change=select_callback)

    with col4:
        random_word = st.button(
            "Random word", key="Random", use_container_width=True
        )
        
    if next_word:
        st.session_state.word_number = (st.session_state.word_number + 1) % number_words

    if previous_word:
        st.session_state.word_number = (st.session_state.word_number - 1) % number_words
        
    if st.session_state.selected_state:
        st.session_state.word_number = int(specific_word) - 1
        st.session_state.selected_state = False
        
    if random_word:
        st.session_state.word_number = random.randint(0, number_words)
    
    # randomly select word number        
    st.markdown(
            f'<div class="blockquote-wrapper"><div class="blockquote"><h1>{chinese_keywords[st.session_state.word_number].word}</span></h1><h4>&mdash; word no. {st.session_state.word_number+1}</em></h4></div></div>',
            unsafe_allow_html=True,
    )
    
    with st.expander("Show Answer"):
        st.markdown(f"<h5 style='text-align: center;'>Word: {chinese_keywords[st.session_state.word_number].word}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: center;'>Pinyin: {chinese_keywords[st.session_state.word_number].pinyin}</h5>", unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: center;'>Translation: {chinese_keywords[st.session_state.word_number].translation}</h5>", unsafe_allow_html=True)
        st.audio(base64.b64decode(chinese_keywords[st.session_state.word_number].pronounciation_audio_bytes.encode('utf-8')))
        st.divider()
        st.markdown(f"<h5 style='text-align: left;'>Definitions</h5>", unsafe_allow_html=True)
        definitions = [defintion for defintion in chinese_keywords[st.session_state.word_number].definitions]
        st.text("\n".join(definitions))
        st.divider()
        st.markdown(f"<h5 style='text-align: left;'>Example Usages</h5>", unsafe_allow_html=True)
        for example_usage in chinese_keywords[st.session_state.word_number].example_usages:
            st.text(f"PY: {example_usage.pinyin}\nCH: {example_usage.chinese}\nEN: {example_usage.english}")
            st.audio(base64.b64decode(example_usage.audio_bytes.encode('utf-8')))
            st.divider()
        
    st.markdown(
        '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
        unsafe_allow_html=True,
    )

with tab2:

    # convert data to pandas dataframe

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("Search in titles, words and answers", value="")
    # 'word', 'pinyin', 'translation', 'definitions', 'example_usages'
    # Filter the dataframe using masks
    m1 = chinese_keywords_df["word"].str.contains(text_search, case=False)
    m2 = chinese_keywords_df["pinyin"].str.contains(text_search, case=False)
    m3 = chinese_keywords_df["translation"].str.contains(text_search, case=False)
    m4 = chinese_keywords_df["definitions"].str.contains(text_search, case=False)
    m5 = chinese_keywords_df["example_usages"].str.contains(text_search, case=False)
    df_search = chinese_keywords_df[m1 | m2 | m3 | m4 | m5]

    # Another way to show the filtered results
    # Show the cards
    N_cards_per_row = 1
    if text_search:
        for n_row, row in df_search.reset_index().iterrows():
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
            # draw the card
            with cols[n_row % N_cards_per_row]:
                # st.caption(f"word {row['No']:0.0f}")
                st.caption(f"{row['word']}")
                st.markdown(f"**{row['pinyin']}**")
                st.markdown(f"{row['translation']}")
                st.markdown(f"{row['definitions']}")
                st.markdown(f"{row['example_usages']}")
                # with st.expander("Answer"):
                #     st.markdown(f"*{row['Answer'].strip()}*")
