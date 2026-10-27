from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth_schemas import LoginSchema,TokenResponse

from app.services.auth.auth_service import autenticar_cliente, criar_token_acesso

from app.database.database import get_db

router = APIRouter(
    prefix = '/login',
    tags = ['Login']
)

@router.post('/',response_model = TokenResponse)
def login_cliente(dados:LoginSchema, db: Session = Depends(get_db)):
    cliente = autenticar_cliente(dados,db)

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "CPF ou senha inválidos"
        )

    token = criar_token_acesso(cliente.id)
    return  TokenResponse(access_token = token)