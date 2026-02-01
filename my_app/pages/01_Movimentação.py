import streamlit as st
from db.connection import SessionLocal
from db.models import Vaga, Estacionamento

if "usuario_id" not in st.session_state:
    st.error("Faça login para acessar esta página")
    st.stop()
    
st.title("Movimentação do Estacionamento")


aba = st.tabs(["Entradas", "Saídas"])

with aba[0]:
    
    
with aba[1]:
    
    
session = SessionLocal()

vagas = (
    session.query(Vaga)
    .join(Estacionamento)
    .all()
)

for vaga in vagas:
    status = "🟥 Ocupada" if vaga.ocupada else "🟩 Livre"
    st.write(f"Vaga {vaga.codigo} - {status}")

session.close()
