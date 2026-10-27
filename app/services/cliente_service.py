from app.services.auth.auth_service import gerar_hash_senha

from sqlalchemy.orm import Session

from sqlalchemy import select
from app.models.cliente_models import Cliente
from app.schemas.cliente_schemas import CreateCliente


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