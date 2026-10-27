from pydantic import BaseModel
from pydantic import ConfigDict

class CreateCliente(BaseModel):
    nome_completo: str
    cpf: str
    idade: int
    endereco: str
    senha_app: str

class ClienteResponse(BaseModel):
    #Transforma o objeto em um dicionario
    model_config = ConfigDict(from_attributes = True)

    id: int
    nome_completo: str
    cpf: str
    idade: int
    endereco: str
