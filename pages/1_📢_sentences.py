import streamlit as st
import streamlit.components.v1 as components
import random
import pandas
# -------------- app config ---------------
st.set_page_config(page_title="Chinese Words Practice", page_icon="🗨️")
st.title("")
# ---------------- functions ----------------
# external css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def select_callback():
    st.session_state.question_number = int(specific_question) - 1
# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.write("**Author: Jason Chan**")
# ---------------- CSS ----------------

local_css("style.css")

# ---------------- SESSION STATE ----------------
    
if "question_number" not in st.session_state:
    st.session_state.question_number = 0

# ---------------- Main page ----------------

tab1, tab2 = st.tabs(["Flashcards", "Search engine"])

rows = pandas.read_csv("./data/chinese_keywords_sample.csv")

question_list = rows['No'].tolist()

with tab1:
    # st.title("Product Owner Interview Questions Flashcards")
    no = len(rows)
    st.caption("Currently we have " + str(no) + " questions in the database")

    # ---------------- Questions & answers logic ----------------

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        next_question = st.button(
            "Next Question", key="Next", use_container_width=True
        )

    with col2:
        previous_question = st.button(
            "Previous Question", key="Previous", use_container_width=True
        )

    with col3:
        specific_question = st.selectbox("Select specific question",
                                     question_list, label_visibility="collapsed", index=None)

    with col4:
        random_question = st.button(
            "Random Question", key="Random", use_container_width=True
        )
        
    if next_question:
        st.session_state.question_number = (st.session_state.question_number + 1) % no

    if previous_question:
        st.session_state.question_number = (st.session_state.question_number - 1) % no
        
    if specific_question:
        st.session_state.question_number = int(specific_question) - 1
        
    if random_question:
        st.session_state.question_number = random.randint(0, 256)
        
    
    # randomly select question number        
    st.markdown(
            f'<div class="blockquote-wrapper"><div class="blockquote"><h1>{rows.iloc[st.session_state.question_number].Question}</span></h1><h4>&mdash; Question no. {st.session_state.question_number+1}</em></h4></div></div>',
            unsafe_allow_html=True,
    )
    
    with st.expander("Show Answer"):
        st.write(rows.iloc[st.session_state.question_number].Answer) 
    st.markdown(
        '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
        unsafe_allow_html=True,
    )
    

with tab2:

    # convert data to pandas dataframe
    df = pandas.DataFrame(rows)

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input("Search in titles, questions and answers", value="")

    # Filter the dataframe using masks
    m1 = df["Topic"].str.contains(text_search, case=False)
    m2 = df["Question"].str.contains(text_search, case=False)
    m3 = df["Answer"].str.contains(text_search, case=False)
    df_search = df[m1 | m2 | m3]

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
                st.caption(f"Question {row['No']:0.0f}")
                st.caption(f"{row['Topic'].strip()}")
                st.markdown(f"**{row['Question'].strip()}**")
                st.markdown(f"{row['Answer'].strip()}")
                with st.expander("Answer"):
                    st.markdown(f"*{row['Answer'].strip()}*")
