from sqlalchemy.orm import Session

from app.models.cliente_models import Cliente
from app.models.conta_models import Conta
from app.schemas.conta_schemas import CreateConta

from app.services.gerador_de_contas import gerar_numero_conta



def criar_conta_service(conta: CreateConta, cliente_id: int, db: Session):
    #verifica se o cliente_id existe ou não 
    cliente_existente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if cliente_existente is None:
        return None 

    numero_conta = gerar_numero_conta(db)

    #Cria objeto conta
    nova_conta = Conta(
        numero = numero_conta,
        tipo = conta.tipo,
        saldo = 0,
        cliente_id = cliente_id,
        senha_cartao = conta.senha_cartao
    )

    #salvar no banco
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)

    #retorna a conta do cliente
    return nova_conta