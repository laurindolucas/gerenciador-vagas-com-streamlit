import streamlit as st 
from db.connection import SessionLocal 
from db.models import *

if "usuario_id" not in st.session_state:
    st.error("Faça login para acessar esta página")
    st.stop()