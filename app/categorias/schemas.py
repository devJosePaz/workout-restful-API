from pydantic import BaseModel, Field
from uuid import UUID

class CategoriaCreate(BaseModel):
    nome: str = Field(..., description="Nome da categoria")

class CategoriaResponse(BaseModel):
    pk_id: UUID
    nome: str

    class Config:
        from_attributes = True
