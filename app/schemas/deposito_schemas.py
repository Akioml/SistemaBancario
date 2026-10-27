from decimal import Decimal

from pydantic import BaseModel, Field

class DepositoCreater(BaseModel):
    conta_id: int = Field(gt = 0)
    valor: Decimal = Field(gt = 0)