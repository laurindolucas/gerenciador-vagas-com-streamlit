import streamlit as st
from db.connection import SessionLocal
from db.models import Usuario
from passlib.context import CryptContext


st.set_page_config(page_title="Login", layout="centered")


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def gerar_hash(senha):
    return pwd_context.hash(senha)


def verificar_senha(senha_digitada, senha_hash):
    return pwd_context.verify(senha_digitada, senha_hash)


def get_db():
    return SessionLocal()


st.title("Sistema de Estacionamento")


aba = st.tabs(["Login", "Cadastro"])


# ================= LOGIN =================

with aba[0]:

    with st.form("login_form"):

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        submit = st.form_submit_button("Entrar")

    if submit:

        if not email or not senha:
            st.warning("Preencha todos os campos")

        else:

            db = get_db()

            try:

                usuario = (
                    db.query(Usuario)
                    .filter(
                        Usuario.email == email,
                        Usuario.ativo == True
                    )
                    .first()
                )

                if usuario and verificar_senha(senha, usuario.senha_hash):

                    st.session_state["usuario_id"] = usuario.id
                    st.session_state["email"] = usuario.email

                    st.success("Login realizado com sucesso")

                    st.switch_page("pages/00_Dashboard.py")

                else:
                    st.error("Email ou senha inválidos")

            finally:
                db.close()


# ================= CADASTRO =================

with aba[1]:

    with st.form("cadastro_form"):

        email_cad = st.text_input("Email", key="cad_email")

        senha_cad = st.text_input(
            "Senha",
            type="password",
            key="cad_senha"
        )

        senha_conf = st.text_input(
            "Confirmar Senha",
            type="password"
        )

        cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:

        if not email_cad or not senha_cad or not senha_conf:

            st.warning("Preencha todos os campos")

        elif senha_cad != senha_conf:

            st.error("As senhas não coincidem")

        elif len(senha_cad) < 6:

            st.error("Senha muito curta (mínimo 6 caracteres)")

        else:

            db = get_db()

            try:

                existe = (
                    db.query(Usuario)
                    .filter(Usuario.email == email_cad)
                    .first()
                )

                if existe:

                    st.error("Esse email já está cadastrado")

                else:

                    senha_hash = gerar_hash(senha_cad)

                    novo_usuario = Usuario(
                        email=email_cad,
                        senha_hash=senha_hash,
                        ativo=True
                    )

                    db.add(novo_usuario)
                    db.commit()

                    st.success("Usuário cadastrado com sucesso")
                    st.info("Agora faça login")

            finally:
                db.close()
