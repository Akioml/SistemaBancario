from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.conta_schemas import ContaResponse, CreateConta
from app.models.cliente_models import Cliente
from app.models.conta_models import Conta

from app.services.conta_service import criar_conta_service
from app.services.consultar_saldo_service import consultar_saldo_service
from app.services.auth.dependencias_auth_services import obter_cliente_atual

from app.database.database import get_db

router = APIRouter(
    prefix = '/contas',
    tags = ['Contas']
)

@router.post('/', response_model = ContaResponse)
def abrir_conta(conta: CreateConta, cliente: Cliente = Depends(obter_cliente_atual), db: Session = Depends(get_db)):
    conta_aberta = criar_conta_service(conta, cliente.id, db)

    if conta_aberta is None:
        raise HTTPException(
            status_code = 409,
            detail = "Conta já esta aberta"
        )

    return conta_aberta

@router.get("/{conta_id}")
def consultar_saldo(
    conta_id: int,
    cliente: Cliente = Depends(obter_cliente_atual),
    db: Session = Depends(get_db)
):

    conta = db.query(Conta).filter(
        Conta.id == conta_id
    ).first()

    if conta is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Conta não encontrada"
        )

    if conta.cliente_id != cliente.id:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Conta não encontrada"
        )
    
    saldo = consultar_saldo_service(conta_id,db)

    return{
        "conta_id": conta_id,
        "saldo": saldo
    }