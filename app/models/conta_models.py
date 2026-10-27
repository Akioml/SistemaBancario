from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Numeric
from app.database.database import Base

"""Banco de dados que armezena as contas dos clientes"""
class Conta(Base):
    __tablename__ = "contas"
    id = Column(Integer, primary_key = True, index = True)
    numero = Column(String(20), nullable = False, unique = True)
    tipo = Column(String(20), nullable = False)
    saldo = Column(Numeric(10, 2), nullable = False)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        unique = False
        )

    bloqueado = Column(Boolean, default=False, nullable=False)
    senha_cartao = Column(String(20), nullable=False)

