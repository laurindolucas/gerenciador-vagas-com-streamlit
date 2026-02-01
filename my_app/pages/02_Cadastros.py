import streamlit as st 
from db.connection import SessionLocal 
from db.models import *


if "usuario_id" not in st.session_state:
    st.error("Faça login para acessar esta página")
    st.stop()

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

if botao:
    
    if proprietario_carro == "" or placa_carro == "" or cor_carro == "" or numero_proprietario == "" or modelo_carro == "":
        st.error("Dados inválidos! por favor preencha as informações corretamente.")
    else:
        session = SessionLocal()
        veiculo = Veiculo(
            placa=placa_carro,
            modelo=modelo_carro,
            cor=cor_carro,
            proprietario=proprietario_carro,
            num_proprietario=numero_proprietario,
            tipo_veiculo_id={"Carro": 1, "Moto": 2, "Caminhão": 3, "Ônibus": 4, "Outro": 5}[tipo_Veiculo]
        )
        session.add(veiculo)
        session.commit()
        st.success("Veículo cadastrado com sucesso!")
