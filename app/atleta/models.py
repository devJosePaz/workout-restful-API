from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.base import BaseModel
from datetime import datetime

class AtletaModel(BaseModel):
    __tablename__ = "atletas"
    
    pk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    categoria_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("categorias.pk_id"))
    categoria: Mapped["CategoriaModel"] = relationship(back_populates="atletas")

    centro_treinamento_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("centros_treinamento.pk_id"))
    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(back_populates="atletas")
