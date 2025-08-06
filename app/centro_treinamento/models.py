from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CentroTreinamentoModel(BaseModel):
    __tablename__ = "centros_treinamento"
    
    pk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)

    atletas: Mapped[list["AtletaModel"]] = relationship("AtletaModel", back_populates="centro_treinamento")
