# 🏋️‍♂️ API de Academia para Competição de CrossFit

Este projeto tem como objetivo a construção de uma **API assíncrona completa** que gerencia os dados de uma academia voltada para competições de **CrossFit**. O foco aqui foi aplicar boas práticas com `FastAPI` e praticar conceitos fundamentais como rotas, métodos HTTP e integração com banco de dados PostgreSQL usando **Docker Compose**.

## 🚀 Tecnologias Utilizadas

- **FastAPI** (API assíncrona com Python)
- **PostgreSQL** (armazenamento de dados)
- **SQLAlchemy** (ORM para acesso ao banco)
- **Docker Compose** (para simular ambiente com banco de dados)
- **Pydantic** (validação de dados)
- **Uvicorn** (servidor ASGI para rodar a API)

## 🧩 Entidades da API

A API foi estruturada para lidar com as seguintes entidades:  

- **Atleta**
- **Centro de Treinamento**
- **Categoria**

## 🔁 Diferença entre PUT e PATCH

Uma das decisões técnicas adotadas foi a seguinte:

- Apenas o recurso **Atleta** possui **método `PATCH`**, ou seja, permite atualizações parciais dos dados.
- Os demais recursos utilizam o método **`PUT`**, que espera a atualização completa da entidade.

## 📦 Como executar

> É necessário ter o **Docker** instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/devJosePaz/workout-restful-API.git
cd workout-restful-API

# 2. Suba o container do banco de dados PostgreSQL
docker-compose up -d

# 3. (Opcional) Ative seu ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 4. Instale as dependências do projeto
pip install -r requirements.txt

# 5. Execute a aplicação
uvicorn app.main:app --reload

# 6. Acesse a documentação interativa da API
# Abra no navegador:
http://localhost:8000/docs




