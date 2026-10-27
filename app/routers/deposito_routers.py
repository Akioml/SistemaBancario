from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.deposito_schemas import DepositoCreater
from app.services.deposito_service import realizar_deposito_service

router = APIRouter(
    prefix = "/depositos",
    tags = ["Depositos"]
)


@router.post("/")
def realizar_deposito(
    deposito: DepositoCreater   ,
    db: Session = Depends(get_db)
):
    resultado = realizar_deposito_service(deposito, db)

    if resultado is None:
        raise HTTPException(
            status_code = 404,
            detail="Conta não encontrada ou bloqueada."
        )

    return resultado
        