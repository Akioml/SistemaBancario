from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from sqlalchemy.orm import Session

from app.models.cliente_models import Cliente
from app.schemas.auth_schemas import LoginSchema

import os 
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não definida no ambiente")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30    

password_hash = PasswordHash.recommended()

def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)

def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    return password_hash.verify(senha_digitada, senha_hash)

def autenticar_cliente(login: LoginSchema, db: Session):

    #Sistema procura o cliente com o CPF informado no banco de dados 
    cliente = db.query(Cliente).filter(
        Cliente.cpf == login.cpf
    ).first()

    #Caso não seja encontrado retorna NONE
    if cliente is None:
        return None

    #A primeira inrformação logi.senha e a senha digitada a segunda e o hash armazenado no banco. A função verifica se elas correspondem
    senha_valida = verificar_senha(
        login.senha_app,
        cliente.senha_app
    )

    #Caso a senha estiver incorreta ou se o CPF não existir retornamos NONE
    if not senha_valida:
        return None

    #Caso a senha estiver correta retornamos o objeto cliente
    return cliente

def criar_token_acesso(cliente_id: int) -> str:
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(cliente_id), "exp": expira_em}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token_acesso(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return payload
    
    except ExpiredSignatureError:
        return None

    except InvalidTokenError:
        return None