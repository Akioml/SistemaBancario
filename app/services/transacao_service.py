from sqlalchemy.orm import Session

from app.models.conta_models import Conta
from app.models.transacao_models import Transacao
from app.schemas.transacao_schemas import CreateTransacao

def criar_transacao_service(transacao: CreateTransacao, cliente_id, db: Session):

    conta_origem = db.query(Conta).filter(
        Conta.id == transacao.conta_origem_id,
        Conta.cliente_id == cliente_id
    ).first()

    if conta_origem is None:
        return None

    if conta_origem.bloqueado:
        return None

    #procura conta destino
    conta_destino = db.query(Conta).filter(
        Conta.id == transacao.conta_destino_id
    ).first()

    if conta_destino is None:
        return None 

    if conta_destino.bloqueado:
        return None

    # verifica se existe saldo suficiente
    if conta_origem.saldo < transacao.valor:
        return None

    # retira o dinheiro da conta de origem 
    conta_origem.saldo -= transacao.valor

    # adiciona o dinheiro da conta de origem a conta de destino
    conta_destino.saldo += transacao.valor

    # cria o registro de transação 
    nova_transacao = Transacao(
            conta_origem_id = transacao.conta_origem_id,
            conta_destino_id = transacao.conta_destino_id,
            tipo= transacao.tipo,
            valor= transacao.valor,
        )

    # adiciona a transacao ao banco
    try:
        db.add(nova_transacao)
        db.commit()
        db.refresh(nova_transacao)
    except Exception:
        db.rollback()
        raise

    return nova_transacao