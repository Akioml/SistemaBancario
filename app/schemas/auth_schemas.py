from pydantic import BaseModel, Field

class LoginSchema(BaseModel):
    cpf: str = Field(min_length = 11, max_length = 11, pattern = r"^\d{11}$")
    senha_app: str = Field(min_length = 1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"