import streamlit as st
from db.connection import SessionLocal
from db.models import Vaga, Estacionamento

st.title("🅿️ Vagas")

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
