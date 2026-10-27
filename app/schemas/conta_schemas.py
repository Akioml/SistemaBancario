from pydantic import BaseModel, Field
from decimal import Decimal

from typing import Literal
from pydantic import ConfigDict

from app.models.cliente_models import Cliente

class CreateConta(BaseModel):
    tipo: Literal["corrente", "poupança"]
    senha_cartao: str = Field(min_length = 4, max_length = 20)


class ContaResponse(BaseModel):
    #Permite que o Pydantic monte o Schema
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    numero: str
    tipo: str
    saldo: Decimal
    cliente_id: int
    bloqueado: bool