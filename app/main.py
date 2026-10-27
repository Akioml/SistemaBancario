from fastapi import FastAPI

from app.database.database import Base, engine

from app.routers.auth_routers import router as auth_router
from app.routers.clientes_routers import router as clientes_router
from app.routers.contas_routers import router as contas_router 
from app.routers.deposito_routers import router as deposito_router
from app.routers.transacoes_routers import router as transacao_router
from app.routers.retornar_cliente import router as buscar_cliente_router
from app.routers.extrato_routers import router as consultar_extrato

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(clientes_router)
app.include_router(contas_router)
app.include_router(deposito_router)
app.include_router(transacao_router)
app.include_router(consultar_extrato)
app.include_router(buscar_cliente_router)