import streamlit as st

if "usuario_id" not in st.session_state:
    st.error("Faça login para acessar esta página")
    st.stop()
    
    
st.set_page_config(
    page_title="Cadastro Page"
)

st.title("Teste de commit 01")
st.write("Essa Paggina sera a dashboard")