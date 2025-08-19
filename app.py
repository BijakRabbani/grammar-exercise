import streamlit as st
from streamlit_shortcuts import shortcut_button 
import pandas as pd
from dotenv import load_dotenv
from google import genai
import os
import random

load_dotenv()

def check_sentence(grammar_concept, word, sentence):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = (
        f"Please check the following sentence for grammatical correctness. "
        f"The sentence should use the word '{word}' and follow the grammar concept '{grammar_concept}'. "
        f"Return 'Correct' if the sentence is correct, or 'Incorrect' if it is not. "
        f"If incorrect, provide a corrected version of the sentence and point out the mistakes. "
        f"Sentence: '{sentence}'"
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(response.text)
    return response.text

@st.dialog(title="Hint")
def show_hint():
    # Display the hint for the grammar concept
    st.write(f"Usage: {st.session_state['grammar_concept_row'][1]}")  
    st.write(f"Example: {st.session_state['grammar_concept_row'][2]}") 
    st.write(f"Word meaning: {st.session_state['word_row'][1]}")  


def click_next():
    del st.session_state['grammar_concept_row'] 
    del st.session_state['grammar_concept'] 
    del st.session_state['word_row']
    del st.session_state['word']
    st.session_state.text_input = ''


def check_gemini_api():
    if 'GEMINI_API_KEY' not in os.environ:
        input_gemini_api()


@st.dialog(title="Please input Gemini API")
def input_gemini_api():
    gemini_api = st.text_input("Gemini API Key", type="password")
    if st.button("Submit", use_container_width=True, key='ssubmit_api'):
        os.environ['GEMINI_API_KEY'] = gemini_api
        st.rerun()


# Streamlit app 
st.title("Grammar Exercise")

# Grammar concept and word
# Read the grammar.xlsx file and pick a random grammar concept
grammar_df = pd.read_excel("grammar.xlsx")
grammar_concept_row = grammar_df.sample(1).iloc[0]
grammar_concept = grammar_concept_row[0]  # Assuming the first column contains the grammar concepts

# Read the vocabulary.xlsx file and pick a random word
vocabulary_df = pd.read_excel("vocabulary.xlsx")
word = vocabulary_df.sample(1).iloc[0, 0] 

# Add a next button to refresh variables only when clicked
if 'grammar_concept' not in st.session_state:
    st.session_state['grammar_concept_row'] = grammar_df.sample(1).iloc[0]
    st.session_state['grammar_concept'] = st.session_state['grammar_concept_row'][0]

if 'word' not in st.session_state:
    st.session_state['word_row'] = vocabulary_df.sample(1).iloc[0]
    st.session_state['word'] = st.session_state['word_row'][0]

if 'button_key_counter' not in st.session_state:
    st.session_state['button_key_counter'] =3

with st.container():
    st.write(f"Grammar Concept: {st.session_state['grammar_concept'] }")
    st.write(f"Word: {st.session_state['word']}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if shortcut_button("Hint", "ctrl+h", hint=True, use_container_width=True):
            show_hint()

    with col2:
        if shortcut_button("Next", "ctrl+n", hint=True, use_container_width=True):
            click_next()


# User input
with st.form(key='form_input'):
    sentence = st.text_input("Create a sentence using the word and grammar concept:", key='text_input')
    submitted = st.form_submit_button("Submit", use_container_width=True)
    if submitted:
        if sentence:

            print(sentence)
            result = check_sentence(
                st.session_state['grammar_concept'], 
                st.session_state['word'], 
                sentence
                )

            is_correct = result.startswith("**Correct**") | result.startswith("Correct") 
            if is_correct:
                st.success(result)
            else:
                st.error(result)
        else:
            st.warning("Please enter a sentence.")

check_gemini_api()