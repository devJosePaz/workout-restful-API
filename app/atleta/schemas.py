from datetime import datetime
from pydantic import Field, PositiveFloat, UUID4, BaseModel
from typing import Annotated
import uuid



from uuid import UUID
from pydantic import Field, BaseModel, PositiveFloat
from typing import Annotated
from datetime import datetime

class AtletaCreate(BaseModel):
    nome: Annotated[str, Field(description="Nome do atleta", example="José", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678910", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=26)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.89)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    
    categoria_id: Annotated[UUID, Field(description="Categoria Id", example="e50c4f29-61c1-4f79-9dc7-2de87ea32150")]
    centro_treinamento_id: Annotated[UUID, Field(description="Centro de Treinamento Id", example="1f01d1d2-ced2-4fa0-9381-023e8282ebf3")]

    class Config:
        extra = "forbid"


class AtletaCreate(BaseModel):
    nome: Annotated[str, Field(description="Nome do atleta", example="José", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678910", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=26)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.89)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    
    categoria_id: Annotated[UUID, Field(description="Categoria Id", example="e50c4f29-61c1-4f79-9dc7-2de87ea32150")]
    centro_treinamento_id: Annotated[UUID, Field(description="Centro de Treinamento Id", example="1f01d1d2-ced2-4fa0-9381-023e8282ebf3")]

    class Config:
        extra = "forbid"

class AtletaResponse(AtletaCreate):
    pk_id: Annotated[UUID4, Field(description="identificador")]
    create_at: Annotated[datetime, Field(description="data de criação")]

    class Config:
        from_attributes = True
