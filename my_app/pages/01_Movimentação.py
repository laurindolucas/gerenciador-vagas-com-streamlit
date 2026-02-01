import streamlit as st
from db.connection import SessionLocal
from db.models import *
from datetime import datetime

if "usuario_id" not in st.session_state:
    st.error("Faça login para acessar esta página")
    st.stop()
    
st.title("Movimentação do Estacionamento")


aba = st.tabs(["Entradas", "Saídas"])


with aba[0]:
    with st.form("entradas_form"):

        placa = st.text_input("Digite a placa do veículo:")
        nome = st.text_input("Digite o nome do proprietário:")

        submit_entrada = st.form_submit_button("Registrar Entrada")

        if submit_entrada:

            if placa == "" or nome == "":
                st.error("Preencha todos os dados.")
            else:

                session = SessionLocal()

                veiculo = session.query(Veiculo).filter_by(
                    placa=placa
                ).first()

                if not veiculo:

                    tipo_padrao = session.query(TipoVeiculo).first()

                    if not tipo_padrao:
                        st.error("Cadastre um tipo de veículo primeiro.")
                        session.close()
                        st.stop()

                    veiculo = Veiculo(
                        placa=placa,
                        proprietario=nome,
                        tipo_veiculo_id=tipo_padrao.id
                    )

                    session.add(veiculo)
                    session.commit()

                vaga = session.query(Vaga).filter_by(
                    ocupada=False
                ).first()

                if not vaga:
                    st.error("Não há vagas disponíveis.")
                    session.close()
                    st.stop()

                entrada = Movimentacao(
                    veiculo_id=veiculo.id,
                    vaga_id=vaga.id,
                    entrada=datetime.now(),
                    status="aberto"
                )

                vaga.ocupada = True

                session.add(entrada)
                session.commit()

                st.success("Entrada registrada com sucesso!")

                session.close()

with aba[1]:
    with st.form("saidas_form"):
        placa_veiculo_saida = st.text_input("Digite a placa do veículo que está saindo:")
        submit_saida = st.form_submit_button("Registrar Saída")

        if submit_saida:

            if placa_veiculo_saida == "":
                st.error("Digite a placa.")
            else:
                session = SessionLocal()
                veiculo = session.query(Veiculo).filter_by(
                    placa=placa_veiculo_saida
                ).first()
                if not veiculo:
                    st.error("Veículo não encontrado.")
                    session.close()
                    st.stop()
                movimentacao = session.query(Movimentacao).filter(
                    Movimentacao.veiculo_id == veiculo.id,
                    Movimentacao.status == "aberto"
                ).first()
                if not movimentacao:
                    st.error("Não há entrada registrada para este veículo.")
                    session.close()
                    st.stop()
                agora = datetime.now()
                movimentacao.saida = agora
                movimentacao.status = "fechado"
                tempo = (agora - movimentacao.entrada).total_seconds() / 3600
                tarifa = session.query(Tarifa).filter_by(
                    estacionamento_id=movimentacao.vaga.estacionamento_id,
                    tipo_veiculo_id=veiculo.tipo_veiculo_id
                ).first()
                if not tarifa:
                    st.error("Tarifa não cadastrada.")
                    session.close()
                    st.stop()
                minutos = (agora - movimentacao.entrada).total_seconds() / 60
                if minutos <= tarifa.tolerancia_minutos:
                    valor = 0
                else:
                    valor = tempo * float(tarifa.valor_hora)
                movimentacao.valor_pago = round(valor, 2)
                session.commit()
                st.success("Saída registrada com sucesso!")
                st.info(f"Valor a pagar: R$ {movimentacao.valor_pago:.2f}")
                session.close()