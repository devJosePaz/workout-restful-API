from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.config.database import get_async_session
from app.atleta.schemas import AtletaCreate, AtletaResponse
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="erro. nenhum atleta encontrado.")

    return atletas

@router.put("/{atleta_id}", response_model=AtletaResponse, status_code=status.HTTP_202_ACCEPTED)
async def atualizar_atleta(atleta_id: UUID, atleta_dados: AtletaCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(AtletaModel).where(AtletaModel.pk_id == atleta_id))
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if atleta.cpf != atleta_dados.cpf:
        result_cpf = await db.execute(select(AtletaModel).where(AtletaModel.cpf == atleta_dados.cpf))
        cpf_duplicado = result_cpf.scalars().first()
        if cpf_duplicado:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="erro. CPF já está em uso")

    atleta.nome = atleta_dados.nome
    atleta.cpf = atleta_dados.cpf
    atleta.idade = atleta_dados.idade
    atleta.peso = atleta_dados.peso
    atleta.altura = atleta_dados.altura
    atleta.sexo = atleta_dados.sexo
    atleta.categoria_id = atleta_dados.categoria_id
    atleta.centro_treinamento_id = atleta_dados.centro_treinamento_id

    try:
        await db.commit()
        await db.refresh(atleta)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="erro: conflito de integridade")

    return atleta




    

    

    
    