from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.base import BaseModel

class CategoriaModel(BaseModel):
    __tablename__ = "categorias"

    pk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    atletas: Mapped[list["AtletaModel"]] = relationship("AtletaModel", back_populates="categoria")
