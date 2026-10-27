from sqlalchemy.orm import Session

from app.models.conta_models import Conta

def realizar_deposito_service(deposito, db: Session):

    conta = db.query(Conta).filter(
        Conta.id == deposito.conta_id
    ).first()

    if conta is None:
        return None

    if conta.bloqueado:
        return None

    conta.saldo += deposito.valor

    db.commit()
    db.refresh(conta)

    return conta