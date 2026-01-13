import streamlit as st 
from db.connection import SessionLocal 
from db.models import Vaga, Estacionamento
import pandas as pd

st.title("Primeiros Cadastros")
st.write("Faça o primeiro cadastro de veiculos aqui")

col1, col2 = st.columns(2)

with col1:
    proprietario_carro= st.text_input(
        "Digite o nome do proprietario do carro:",
        placeholder="ex: Caleb Araujo..."   
    )
     
    placa_carro= st.text_input(
        "Digite a placa do carro:",
        placeholder="ex: DEV 1399..."   
    )
    
    cor_carro= st.text_input(
        "Digite a cor do carro:",
        placeholder="ex: Vermelho..."   
    )
    
    
with col2:
    numero_proprietario= st.text_input(
        "Digite o número do proprietario do carro:",
        placeholder="ex: (81) 9 98855-3344..."   
    )
    tipo_Veiculo= st.selectbox(
        "Selecione o tipo do veiculo?", 
        ("Carro", "Moto", "Caminhão", "Ônibus", "Outro") 
        )
    
    modelo_carro= st.text_input(
        "Digite o modelo do carro:",
        placeholder="ex: Civic..."   
    )
    
confirmarButton= st.container(horizontal=True, horizontal_alignment="center")

botao = confirmarButton.button("Cadastar")
    
