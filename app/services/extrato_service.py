from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.conta_models import Conta
from app.models.transacao_models import Transacao

def consultar_extrato(conta_id: int, cliente_id: int, db: Session):

    conta = db.query(Conta).filter(
        Conta.id == conta_id,
        Conta.cliente_id == cliente_id
    ).first()

    if conta is None:
        return None


    transacoes = db.query(Transacao).filter(
        or_(
            Transacao.conta_origem_id == conta_id,
            Transacao.conta_destino_id == conta_id
        )
    ).order_by(
        Transacao.data_hora.desc()
    ).all()

    return transacoes