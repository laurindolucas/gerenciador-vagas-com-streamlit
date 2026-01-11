from db.connection import SessionLocal
from db.models import TipoVeiculo

session = SessionLocal()

carro = TipoVeiculo(nome="Kombi")
session.add(carro)
session.commit()

result = session.query(TipoVeiculo).all()
print([t.nome for t in result])

session.close()
