from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from app.database.database import get_db

from app.services.auth.auth_service import validar_token_acesso
from app.models.cliente_models import Cliente

security = HTTPBearer()

def obter_cliente_atual(credencias: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):

    
    token = credencias.credentials

    payload = validar_token_acesso(token)

    if not payload:
        raise HTTPException(            
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token invalído ou expirado",
            headers = {"WWW-Authenticate": "Bearer"}
            )

    
    cliente_id = payload.get("sub")

    if not cliente_id:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token sem identificação do cliente",
            headers = {"www-Authenticate": "Bearer"}
        )

    cliente = db.query(Cliente).filter(
        Cliente.id == int(cliente_id)
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Cliente não encontrado",
            headers = {"www-Authenticate": "Bearer"}
        )

    return cliente
