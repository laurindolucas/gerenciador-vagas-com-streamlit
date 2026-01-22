
import streamlit as st 
from db.connection import SessionLocal 
from db.models import *
import pandas as pd
from datetime import time

if "estacionamento_id" not in st.session_state:
    st.session_state["estacionamento_id"] = None

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
    totalVagas= st.number_input(
        "Digite o total de vagas do Estacionamento:",        step=1   
    )
    statusAtivo= st.selectbox(
        "O Estacionamento está ativo?", 
        ("Sim", "Não") 
        )
    
    
confirmarButton= st.container(horizontal=True, horizontal_alignment="center")

botao = confirmarButton.button("Confirmar Configurações")


if botao:
    
    if nomeEstacionamento == "" or enderecoEstacionamento == " " or totalVagas == 0:
        st.error("Dados inválidos! por favor preencha as informações corretamente.")
    else:
        session = SessionLocal()
        estacionamento = Estacionamento(
            nome=nomeEstacionamento,
            endereco=enderecoEstacionamento,
            total_vagas=int(totalVagas),
            ativo=True if statusAtivo == "Sim" else False
        )
        session.add(estacionamento)
        session.commit()
        st.session_state["estacionamento_id"] = estacionamento.id

        
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

tabela_config_tarifas = pd.DataFrame(
    [
        {"Tipos De Veiculos": "Carro", "Valor por hora" : 30, "Minutos de Tolerancia" : 20},
        {"Tipos De Veiculos": "Moto", "Valor por hora" : 20, "Minutos de Tolerancia" : 10},
        {"Tipos De Veiculos": "Caminhão", "Valor por hora" : 50, "Minutos de Tolerancia" : 30},
        {"Tipos De Veiculos": "Bicicleta", "Valor por hora" : 10, "Minutos de Tolerancia" : 10},

    ]
)
editor_tabela = st.data_editor(tabela_config_tarifas, num_rows="dynamic")

confirm_tarifas = st.container(horizontal=True, horizontal_alignment="center")
salvar_tarifas = confirm_tarifas.button("Confirmar configuração das tarifas")

if salvar_tarifas:
    if not st.session_state["estacionamento_id"]:
        st.error("Crie o estacionamento antes de configurar as tarifas.")
        st.stop()

    session = SessionLocal()

    try:
        for _, row in editor_tabela.iterrows():
            nome_tipo = row["Tipos De Veiculos"].strip()
            valor_hora = row["Valor por hora"]
            tolerancia = row["Minutos de Tolerancia"]

            tipo = session.query(TipoVeiculo).filter_by(nome=nome_tipo).first()

            if not tipo:
                tipo = TipoVeiculo(nome=nome_tipo)
                session.add(tipo)
                session.flush()  

            # -----------------------------
            tarifa = session.query(Tarifa).filter_by(
                estacionamento_id=st.session_state["estacionamento_id"],
                tipo_veiculo_id=tipo.id
            ).first()

            if tarifa:
                tarifa.valor_hora = valor_hora
                tarifa.tolerancia_minutos = tolerancia
            else:
                nova_tarifa = Tarifa(
                    estacionamento_id=st.session_state["estacionamento_id"],
                    tipo_veiculo_id=tipo.id,
                    valor_hora=valor_hora,
                    tolerancia_minutos=tolerancia
                )
                session.add(nova_tarifa)

        session.commit()
        st.success("Tipos de veículos e tarifas configurados com sucesso!")

    except Exception as e:
        session.rollback()
        st.error(f"Erro ao salvar configurações: {e}")

    finally:
        session.close()
