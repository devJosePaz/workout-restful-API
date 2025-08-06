from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.config.database import get_async_session
from app.atleta.schemas import AtletaCreate, AtletaResponse, AtletaUpdate
from app.atleta.models import AtletaModel
from uuid import UUID

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.post("/atleta", response_model=AtletaResponse, status_code=status.HTTP_201_CREATED)
async def criar_atleta(atleta: AtletaCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(AtletaModel).where(AtletaModel.cpf == atleta.cpf))
    atleta_existente = result.scalars().first()

    if atleta_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="erro: o CPF digitado indica que o atleta já está cadastrado")

    novo_atleta = AtletaModel(
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        categoria_id=atleta.categoria_id,
        centro_treinamento_id=atleta.centro_treinamento_id
    )

    db.add(novo_atleta)
    await db.commit()
    await db.refresh(novo_atleta)

    return novo_atleta


@router.get("/atletas", response_model=list[AtletaResponse], status_code=status.HTTP_200_OK)
async def listar_atletas(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(AtletaModel))
    atletas = result.scalars().all()

    if not atletas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="erro. atleta não encontrado.")

    return atletas

@router.patch("/{atleta_id}", response_model=AtletaUpdate, status_code=status.HTTP_202_ACCEPTED)
async def atualizar_atleta(atleta_id: UUID, atleta_dados: AtletaUpdate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(AtletaModel).where(AtletaModel.pk_id == atleta_id))
    atleta = result.scalars().first()

    try:
        await db.commit()
        await db.refresh(atleta)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="erro: conflito de integridade")

    return atleta




    

    

    
    