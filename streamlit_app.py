import streamlit as st

st.title("🎯 Lucky Quiz Game")
st.write("Welcome to your quiz app!")

name = st.text_input("Apna naam likho:")

if st.button("Start Quiz"):
    st.success(f"Welcome {name}, Quiz start ho rahi hai!")
