from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.transacao_schemas import TransacaoResponse
from app.models.cliente_models import Cliente

from app.services.extrato_service import consultar_extrato
from app.services.auth.dependencias_auth_services import obter_cliente_atual

router = APIRouter(
    prefix = "/consultaExtrato",
    tags = ["Extrato"]
)

@router.get("/{conta_id}/extrato", response_model = list[TransacaoResponse],)
def vericiar_extato(
    conta_id: int,
    cliente_id: Cliente = Depends(obter_cliente_atual),
    db: Session = Depends(get_db)
):
    resultado = consultar_extrato(conta_id, cliente_id.id, db)

    if resultado is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Estrato não disponivel"
        )
    
    return resultado