from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.cliente_schemas import (
    ClienteResponse,
)
from app.services.cliente_service import ClienteService

router = APIRouter(
    prefix = "/todosClientes",
    tags = ["Retorno"]
)

@router.get("/", response_model = list[ClienteResponse])
def listar_cliente(
    db: Session = Depends(get_db) 
):
    retorno = ClienteService.listar_todos(db)

    if retorno is None:
        raise HTTPException(
            status_code = 404,
            detail = "Cliente não encontrado"
    )

    return retorno

# 2. Rota para buscar cliente por ID
@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente_por_id(cliente_id: int, db: Session = Depends(get_db)):
  # CORREÇÃO: Usando ClienteService (e não ClienteResponse)
  cliente = ClienteService.buscar_por_id(cliente_id, db)

  if not cliente:
    raise HTTPException(
    status_code=404, 
    detail="Cliente não encontrado"
    )

  return cliente