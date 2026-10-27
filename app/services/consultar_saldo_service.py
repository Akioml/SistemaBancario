from sqlalchemy.orm import Session

from app.models.conta_models import Conta

def consultar_saldo_service(conta_id: int, db: Session):
    conta = db.query(Conta).filter(
        Conta.id == conta_id
    ).first()

    if conta is None:
        return None 

    return conta.saldo