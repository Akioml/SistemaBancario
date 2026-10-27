from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.cliente_schemas import ClienteResponse, CreateCliente

from app.services.cliente_service import criar_cliente_service, excluir_cliente_service 

from app.database.database import get_db

router = APIRouter(
    prefix = '/clientes',
    tags = ['Clientes']
)

@router.post('/', response_model = ClienteResponse)
def criar_cliente(cliente: CreateCliente, db: Session = Depends(get_db)):
    cliente_criado = criar_cliente_service(cliente, db)

    if cliente_criado is None:
        raise HTTPException(
            status_code=409,
            detail="Cliente já cadastrado."
        )

    return cliente_criado

@router.delete("/{cliente_id}")
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    return excluir_cliente_service(cliente_id, db)
