import streamlit as st
import pandas as pd
from sqlalchemy import func
from db.connection import SessionLocal
from db.models import (
    Estacionamento,
    Vaga,
    Veiculo,
    Movimentacao,
    Tarifa
)


if "usuario_id" not in st.session_state:
    st.error("Faça login para acessar a dashboard")
    st.stop()


st.set_page_config(
    page_title="Dashboard - Estacionamento",
    layout="wide"
)

st.title("Dashboard do Estacionamento")

session = SessionLocal()

estacionamento = session.query(Estacionamento).filter_by(
    usuario_id=st.session_state["usuario_id"],
    ativo=True
).first()

if not estacionamento:
    st.warning("Nenhum estacionamento ativo encontrado.")
    session.close()
    st.stop()


total_vagas = session.query(Vaga).filter_by(
    estacionamento_id=estacionamento.id
).count()

vagas_ocupadas = session.query(Vaga).filter_by(
    estacionamento_id=estacionamento.id,
    ocupada=True
).count()

vagas_livres = total_vagas - vagas_ocupadas


veiculos_ativos = session.query(Movimentacao).filter_by(
    status="aberto"
).count()


faturamento = session.query(
    func.sum(Movimentacao.valor_pago)
).filter(
    Movimentacao.status == "fechado"
).scalar() or 0


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total de Vagas", total_vagas)
col2.metric("Livres", vagas_livres)
col3.metric("Ocupadas", vagas_ocupadas)
col4.metric("Veículos Ativos", veiculos_ativos)
col5.metric("Faturamento", f"R$ {faturamento:.2f}")


st.divider()




st.subheader("Veículos no Estacionamento")

abertos = session.query(
    Movimentacao,
    Veiculo,
    Vaga
).join(Veiculo).join(Vaga).filter(
    Movimentacao.status == "aberto"
).all()


if abertos:

    dados_abertos = []

    for mov, veic, vaga in abertos:

        dados_abertos.append({
            "Placa": veic.placa,
            "Proprietário": veic.proprietario,
            "Vaga": vaga.codigo,
            "Entrada": mov.entrada.strftime("%d/%m/%Y %H:%M")
        })

    df_abertos = pd.DataFrame(dados_abertos)

    st.dataframe(df_abertos, use_container_width=True)

else:
    st.info("Nenhum veículo no momento.")


st.divider()




st.subheader("Últimas Movimentações")


ultimas = session.query(
    Movimentacao,
    Veiculo,
    Vaga
).join(Veiculo).join(Vaga).order_by(
    Movimentacao.created_at.desc()
).limit(15).all()


dados_ultimas = []

for mov, veic, vaga in ultimas:

    dados_ultimas.append({
        "Placa": veic.placa,
        "Vaga": vaga.codigo,
        "Status": mov.status,
        "Entrada": mov.entrada.strftime("%d/%m/%Y %H:%M"),
        "Saída": mov.saida.strftime("%d/%m/%Y %H:%M") if mov.saida else "-",
        "Valor": f"R$ {mov.valor_pago:.2f}" if mov.valor_pago else "-"
    })


df_ultimas = pd.DataFrame(dados_ultimas)

st.dataframe(df_ultimas, use_container_width=True)


st.divider()




st.subheader("Faturamento Diário")

faturamento_dia = session.query(
    func.date(Movimentacao.saida),
    func.sum(Movimentacao.valor_pago)
).filter(
    Movimentacao.status == "fechado"
).group_by(
    func.date(Movimentacao.saida)
).all()


if faturamento_dia:

    df_fat = pd.DataFrame(
        faturamento_dia,
        columns=["Data", "Faturamento"]
    )

    st.line_chart(df_fat.set_index("Data"))

else:
    st.info("Sem faturamento registrado.")


st.divider()



st.subheader("Tarifas Cadastradas")

tarifas = session.query(
    Tarifa,
    Veiculo,
    Estacionamento
).join(Estacionamento).join(
    Veiculo, Veiculo.tipo_veiculo_id == Tarifa.tipo_veiculo_id
).all()


dados_tarifas = []

for tarifa, veic, est in tarifas:

    dados_tarifas.append({
        "Estacionamento": est.nome,
        "Tipo Veículo": veic.tipo.nome,
        "Valor/Hora": f"R$ {float(tarifa.valor_hora):.2f}",
        "Tolerância (min)": tarifa.tolerancia_minutos
    })


df_tarifas = pd.DataFrame(dados_tarifas)

st.dataframe(df_tarifas, use_container_width=True)


session.close()
