# Gerenciador de Estacionamento

Um **gerenciador de estacionamento** desenvolvido em **Python**, utilizando **Streamlit** para a interface web e **PostgreSQL** como banco de dados, hospedado no **Supabase**.

O projeto tem como objetivo simular o controle de um estacionamento, permitindo gerenciar veículos, vagas e persistência de dados em um ambiente real de banco de dados, servindo como um projeto prático para estudos em **Python**, **SQL**, **ORM** e **deploy de banco em nuvem**.

---

## Tecnologias Utilizadas

- **Python**
- **Streamlit** – Interface web
- **SQLAlchemy** – ORM para comunicação com o banco
- **PostgreSQL** – Banco de dados
- **Supabase** – Hospedagem do banco de dados
- **python-dotenv** – Gerenciamento de variáveis de ambiente

---

## Como Executar o Projeto

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/laurindolucas/gerenciador-vagas-com-streamlit.git
cd gerenciador-vagas-com-streamlit
```

### 2️⃣ Crie e ative o ambiente virtual `(.venv)`
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Instale as dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:
```bash
pip install streamlit python-dotenv sqlalchemy psycopg2-binary
```
### 4️⃣ Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto e adicione a URL de conexão com o banco do Supabase:
```bash
DATABASE_URL = suaurl
```
#### Importante:
Nunca suba o arquivo .env para o GitHub.
Adicione-o ao .gitignore.

### 5️⃣ Execute a aplicação
```bash
streamlit run app.py
```



