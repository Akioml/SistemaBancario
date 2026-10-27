from fastapi import HTTPException
from app.services.auth.auth_service import gerar_hash_senha

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.cliente_models import Cliente
from app.schemas.cliente_schemas import CreateCliente
from app.models.conta_models import Conta

def criar_cliente_service(cliente: CreateCliente, db: Session):
    #Verfica se CPF já existe
    cliente_existente = db.query(Cliente).filter(
        Cliente.cpf == cliente.cpf
        ).first()
    
    if cliente_existente:
        return None

    #Cria objeto Cliente
    novo_cliente = Cliente(
        nome_completo = cliente.nome_completo,
        cpf = cliente.cpf,
        idade = cliente.idade,
        endereco = cliente.endereco,
        senha_app = gerar_hash_senha(cliente.senha_app)
    )

    #salvar no banco
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    #retorna cliente
    return novo_cliente

class ClienteService:

  @staticmethod
  def listar_todos(db: Session):
    # Retorna uma lista com todos os clientes
    stmt = select(Cliente)
    return db.scalars(stmt).all()

  @staticmethod
  def buscar_por_id(cliente_id: int, db: Session):
    # Busca um cliente específico pelo ID
    cliente = db.get(Cliente, cliente_id)
    return cliente


def excluir_cliente_service(cliente_id: int, db: Session):
    # Busca o cliente pelo ID
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    # Verifica se o cliente existe
    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    # Verifica se o cliente possui alguma conta bancária
    conta = db.query(Conta).filter(
        Conta.cliente_id == cliente_id
    ).first()

    # Exclui o cliente do banco de dados
    db.delete(cliente)
    db.commit()

    return {"mensagem": "Cliente excluído com sucesso"}
