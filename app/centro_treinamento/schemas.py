from pydantic import Field, BaseModel
from uuid import UUID

class CentroTreinamentoCreate(BaseModel):
    nome: str = Field(..., description="Nome do centro de trienamento")
    endereco: str = Field(..., description="Endereço do centro de treinamento")
    proprietario: str = Field(..., description="Proprietáriod do centro de trienamento")

class CentroTreinamentoResponse(CentroTreinamentoCreate):
    pk_id : UUID

    class Config:
        from_attributes = True




