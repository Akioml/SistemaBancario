from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cliente_models import Cliente
from app.schemas.transacao_schemas import CreateTransacao
from app.services.transacao_service import criar_transacao_service
from app.services.auth.dependencias_auth_services import obter_cliente_atual

router = APIRouter(
    prefix = "/transacao",
    tags = ["Transacao"]
)

@router.post("/")
def realizar_transferencia(
    transacao: CreateTransacao,
    cliente: Cliente = Depends(obter_cliente_atual),
    db: Session = Depends(get_db)
):
    resultado = criar_transacao_service(transacao, cliente.id, db)

    if resultado is None:
        raise HTTPException(
            status_code = 404,
            detail = "Conta não encontrada ou transferência não permitida."
        )

    return resultado