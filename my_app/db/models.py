from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Numeric,
    TIMESTAMP,
    UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class TipoVeiculo(Base):
    __tablename__ = "tipos_veiculos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(30), unique=True, nullable=False)

    veiculos = relationship("Veiculo", back_populates="tipo")
    tarifas = relationship("Tarifa", back_populates="tipo")


class Estacionamento(Base):
    __tablename__ = "estacionamentos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String)
    total_vagas = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    vagas = relationship("Vaga", back_populates="estacionamento")
    tarifas = relationship("Tarifa", back_populates="estacionamento")


class Vaga(Base):
    __tablename__ = "vagas"
    __table_args__ = (
        UniqueConstraint("codigo", "estacionamento_id"),
    )

    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), nullable=False)
    estacionamento_id = Column(Integer, ForeignKey("estacionamentos.id"), nullable=False)
    ocupada = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    estacionamento = relationship("Estacionamento", back_populates="vagas")
    movimentacoes = relationship("Movimentacao", back_populates="vaga")
    tipos_aceitos = relationship("VagaTipoVeiculo", back_populates="vaga")


class VagaTipoVeiculo(Base):
    __tablename__ = "vaga_tipos_veiculos"
    __table_args__ = (
        UniqueConstraint("vaga_id", "tipo_veiculo_id"),
    )

    id = Column(Integer, primary_key=True)
    vaga_id = Column(Integer, ForeignKey("vagas.id"), nullable=False)
    tipo_veiculo_id = Column(Integer, ForeignKey("tipos_veiculos.id"), nullable=False)

    vaga = relationship("Vaga", back_populates="tipos_aceitos")
    tipo = relationship("TipoVeiculo")


class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True)
    placa = Column(String(10), unique=True, nullable=False)
    modelo = Column(String(50))
    cor = Column(String(30))
    proprietario = Column(String(100))
    tipo_veiculo_id = Column(Integer, ForeignKey("tipos_veiculos.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    tipo = relationship("TipoVeiculo", back_populates="veiculos")
    movimentacoes = relationship("Movimentacao", back_populates="veiculo")


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    vaga_id = Column(Integer, ForeignKey("vagas.id"), nullable=False)

    entrada = Column(TIMESTAMP(timezone=True), nullable=False)
    saida = Column(TIMESTAMP(timezone=True))
    valor_pago = Column(Numeric(10, 2))
    status = Column(String(20), default="aberto")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    veiculo = relationship("Veiculo", back_populates="movimentacoes")
    vaga = relationship("Vaga", back_populates="movimentacoes")


class Tarifa(Base):
    __tablename__ = "tarifas"
    __table_args__ = (
        UniqueConstraint("estacionamento_id", "tipo_veiculo_id"),
    )

    id = Column(Integer, primary_key=True)
    estacionamento_id = Column(Integer, ForeignKey("estacionamentos.id"), nullable=False)
    tipo_veiculo_id = Column(Integer, ForeignKey("tipos_veiculos.id"), nullable=False)
    valor_hora = Column(Numeric(10, 2), nullable=False)
    tolerancia_minutos = Column(Integer, default=10)

    estacionamento = relationship("Estacionamento", back_populates="tarifas")
    tipo = relationship("TipoVeiculo", back_populates="tarifas")
