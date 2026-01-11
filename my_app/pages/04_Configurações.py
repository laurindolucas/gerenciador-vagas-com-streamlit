
import streamlit as st 
from db.connection import SessionLocal 
from db.models import Estacionamento, Vaga

st.title("Configurações do Estacionamento")

st.header("Dados do Estacionamento")
col1, col2 = st.columns(2)

with col1:
    
    nomeEstacionamento= st.text_input(
        "Digite o nome do Estacionamento:",
        placeholder="Digite o nome aqui..."   
    )
    enderecoEstacionamento= st.text_input(
        "Digite o endereço do Estacionamento:",
        placeholder="Digite o endereço aqui..."
    )

with col2:
    totalVagas= st.text_input(
        "Digite o total de vagas do Estacionamento:",
        placeholder="Digite o total de vagas aqui..."   
    )
    statusAtivo= st.selectbox(
        "O Estacionamento está ativo?", 
        ("Sim", "Não") 
        )
    
confirmarButton= st.button("Confirmar Configurações")

if confirmarButton:
    session = SessionLocal()
    estacionamento = Estacionamento(
        nome=nomeEstacionamento,
        endereco=enderecoEstacionamento,
        total_vagas=int(totalVagas),
        ativo=True if statusAtivo == "Sim" else False
    )
    session.add(estacionamento)
    session.commit()
    
    for i in range(1, int(totalVagas) + 1):
        vagaconfig = Vaga(
            codigo=f"EST-{i}",  
            estacionamento_id=estacionamento.id
        )
        session.add(vagaconfig)
    session.commit()
    
    st.success(f"{totalVagas} vagas criadas automaticamente.")

    st.success("Configurações salvas com sucesso!")
    session.close()

st.header("Configurações de Tarifas")

