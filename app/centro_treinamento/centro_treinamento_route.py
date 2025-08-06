from fastapi import APIRouter, HTTPException, Depends, status
from app.centro_treinamento.schemas import CentroTreinamentoCreate, CentroTreinamentoResponse
from app.centro_treinamento.models import  CentroTreinamentoModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_async_session
from uuid import UUID



router = APIRouter(prefix="/centros_treinamento", tags=["Centros de treinamento"])

@router.post("/centro_treinamento", response_model=CentroTreinamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_centro_treinamento(centro_treinamento: CentroTreinamentoCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CentroTreinamentoModel).where(CentroTreinamentoModel.nome == centro_treinamento.nome))
    centro_treinamento_existente = result.scalars().first()

    if centro_treinamento_existente:
        raise HTTPException(status_code=409, detail="erro: centro de treinamento ja existente")

    novo_centro_treinamento = CentroTreinamentoModel(
        nome=centro_treinamento.nome,
        endereco=centro_treinamento.endereco,
        proprietario=centro_treinamento.proprietario
    )

    db.add(novo_centro_treinamento)
    await db.commit()
    await db.refresh(novo_centro_treinamento)

    return novo_centro_treinamento

@router.get("/centros_treinamento", response_model=list[CentroTreinamentoResponse], status_code=status.HTTP_200_OK)
async def listar_centros_treinamento(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CentroTreinamentoModel))
    centros_treinamento = result.scalars().all()

    if not centros_treinamento:
        raise HTTPException(status_code=404, detail="erro: nenhum centro de treinamento encontrado")

    return centros_treinamento

@router.get("/{centro_treinamento_id}", response_model=CentroTreinamentoResponse, status_code=status.HTTP_200_OK)
async def listar_centro_treinamento_id(centro_treinamento_id: UUID, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CentroTreinamentoModel).where(CentroTreinamentoModel.pk_id == centro_treinamento_id))
    centro_treinamento = result.scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=404, detail="erro: centro de treinamento não encontrado com o ID digitado")

    return centro_treinamento

@router.put("/{centro_treinamento_id}", response_model=CentroTreinamentoResponse, status_code=status.HTTP_202_ACCEPTED)
async def atualizar_centro_treinamento(centro_treinamento_id: UUID, centro_treinamento_dados: CentroTreinamentoCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CentroTreinamentoModel).where(CentroTreinamentoModel.pk_id == centro_treinamento_id))
    centro_treinamento = result.scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=404, detail="erro: centro de treinamento não encontrado com o ID digitado.")

    centro_treinamento.nome = centro_treinamento_dados.nome
    centro_treinamento.endereco = centro_treinamento_dados.endereco
    centro_treinamento.proprietario = centro_treinamento_dados.proprietario

    try:
        await db.commit()
        await db.refresh(centro_treinamento)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=404, detail="erro: nome já está sendo usado por outro centro de treinamento.")

    return centro_treinamento

@router.delete("/{centro_treinamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_centro_treinamento(centro_treinamento_id: UUID, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CentroTreinamentoModel).where(CentroTreinamentoModel.pk_id == centro_treinamento_id))
    centro_treinamento = result.scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=404, detail="erro: centro de treinamento não encontrado com o Id digitado.")

    await db.delete(centro_treinamento)
    await db.commit()



    



    

    
    


    








    

