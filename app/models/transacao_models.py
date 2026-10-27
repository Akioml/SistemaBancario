from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from app.database.database import Base
from datetime import datetime

"""Banco de dados que armezenara as transações feitas"""
class Transacao(Base):
    __tablename__ = "transacoes"
    id = Column(Integer, primary_key = True, index = True)

    conta_origem_id = Column(
        Integer,
        ForeignKey("contas.id"),
        nullable = True
    )

    conta_destino_id = Column(
        Integer,
        ForeignKey("contas.id"),
        nullable = False
    )

    tipo = Column(String(20), nullable = False)
    valor = Column(Numeric(10, 2), nullable = False)

    data_hora = Column(
        DateTime,
        default = datetime.now,
        nullable = False
    )