import streamlit as st
from streamlit_shortcuts import button, add_keyboard_shortcuts 
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
    # st.rerun()


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


with st.container():
    st.write(f"Grammar Concept: {st.session_state['grammar_concept'] }")
    st.write(f"Word: {st.session_state['word']}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        button("Hint", "ctrl+h", show_hint, hint=True, use_container_width=True)

    with col2:
        button("Next", "ctrl+n", click_next, hint=True, use_container_width=True)


# User input
sentence = st.text_input("Create a sentence using the word and grammar concept:", key='text_input')
# def click_submit(sentence):
#     if sentence:

#         print(sentence)
#         result = check_sentence(
#             st.session_state['grammar_concept'], 
#             st.session_state['word'], 
#             sentence
#             )

#         is_correct = result.startswith("**Correct**") | result.startswith("Correct") 
#         if is_correct:
#             st.success(result)
#         else:
#             st.error(result)
#     else:
#         st.warning("Please enter a sentence.")
# button("Submit", "ctrl+enter", click_submit, args=(sentence,), hint=True, use_container_width=True)
if st.button("Submit", use_container_width=True):
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
