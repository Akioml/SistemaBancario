from decimal import Decimal
from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class CreateTransacao(BaseModel):
    """Transforma o objeto em um dicionario"""
    model_config = ConfigDict(from_attributes = True)

    conta_origem_id: int = Field(gt = 0)
    conta_destino_id: int = Field(gt = 0)
    tipo: Literal["transferencia", "pix"]
    valor:Decimal = Field(gt = 0)

class TransacaoResponse(BaseModel):
    id: int 
    conta_origem_id: int | None
    conta_destino_id: int
    tipo: str
    valor: Decimal
    data_hora: datetime