from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_async_session
from app.categorias.schemas import CategoriaCreate, CategoriaResponse
from app.categorias.models import CategoriaModel
from uuid import UUID


router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/categoria", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def criar_categoria(categoria: CategoriaCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CategoriaModel).where(CategoriaModel.nome == categoria.nome))
    categoria_existente = result.scalars().first()

    if categoria_existente:
        raise HTTPException(status_code=409, detail="erro: categoria já cadastrada")

    nova_categoria = CategoriaModel(
        nome=categoria.nome
    )

    db.add(nova_categoria)
    await db.commit()
    await db.refresh(nova_categoria)

    return nova_categoria



@router.get("/categorias", response_model=list[CategoriaResponse], status_code=status.HTTP_200_OK)
async def listar_categorias(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CategoriaModel))
    categorias = result.scalars().all()

    if not categorias:
        raise HTTPException(status_code=404, detail="erro: nenhuma categoria cadastrada")

    return categorias


@router.get("/{categoria_id}", response_model=CategoriaResponse, status_code=status.HTTP_200_OK)
async def listar_categoria_id(categoria_id: UUID, db: AsyncSession = Depends(get_async_session)):
    result =  await db.execute(select(CategoriaModel).where(CategoriaModel.pk_id == categoria_id))
    categoria = result.scalars().first()

    if not categoria:
        raise HTTPException(status_code=404, detail="erro: categoria não encontrada com o ID digitado")

    return categoria


@router.put("/{categoria_id}", response_model=CategoriaResponse, status_code=status.HTTP_202_ACCEPTED)
async def atualizar_categoria(categoria_dados: CategoriaCreate, categoria_id: UUID, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CategoriaModel).where(CategoriaModel.pk_id == categoria_id))
    categoria = result.scalars().first()

    if not categoria:
        raise HTTPException(status_code=404, detail="erro: categoria não encontrada com o Id digitado")

    categoria.nome = categoria_dados.nome

    try:
        await db.commit()
        await db.refresh(categoria)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="erro: nome já está sendo usado por outra categoria.")

    return categoria

@router.delete("/{categoria_id}", response_model=CategoriaResponse, status_code=status.HTTP_204_NO_CONTENT)
async def deletar_categoria(categoria_id: UUID, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(CategoriaModel).where(CategoriaModel.pk_id == categoria_id))
    categoria = result.scalars().first()

    if not categoria:
        raise HTTPException(status_code=404, detail="erro: categoria não encontrada")

    await db.delete(categoria)
    await db.commit()




    
    
