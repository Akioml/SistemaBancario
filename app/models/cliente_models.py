from sqlalchemy import Column, String, Integer
from app.database.database import Base

"""Banco de dados que armezenara as infomações dos clientes"""
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key = True, index = True)
    nome_completo = Column(String(100), nullable = False)
    cpf = Column(String(11), nullable= False, unique = True)
    idade = Column(Integer, nullable = False)
    endereco = Column(String(100), nullable = False)
    senha_app = Column(String(255), nullable = False)
