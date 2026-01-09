import streamlit as st

col1, col2 = st.columns(2)

with col1:
    text_input = st.text_input(
        "Enter some text 👇",
        placeholder="Digite algo aqui..."
    )

    if text_input:
        st.write("You entered:", text_input)
