from fastapi import FastAPI
from app.config.database import engine
from app.categorias.categoria_route import router as categoria_router
from app.centro_treinamento.centro_treinamento_route import router as centro_treinamento_route
from app.atleta.atleta_route import router as atleta_router
from app.base import BaseModel

from app.atleta.models import AtletaModel
from app.centro_treinamento.models import CentroTreinamentoModel
from app.categorias.models import CategoriaModel


app = FastAPI(title="WorkOutAPI")

app.include_router(categoria_router)
app.include_router(centro_treinamento_route)
app.include_router(atleta_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
