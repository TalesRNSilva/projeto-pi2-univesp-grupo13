### Módulo que vai gerenciar as rotas e instanciar o APP
from db import *
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from modelos.responsavel import Responsavel
from modelos.obra import Obra
from schema.responsavel import *
from schema.obra import *
from mock_data_seed import inserir_dados_teste
from utils import *

## Para rodar: 'uvicorn main:app --reload' na pasta /app/

app = FastAPI()
# inserir_dados_teste()

################################################ Rotas da entidade Obras ################################################
@app.get('/obras', response_model = list[ObraResponse])
async def get_obras(p:int = Query(default = 1, ge = 1), 
                    per_page:int = Query(default = 12, ge = 1, le = 100), 
                    session = Depends(get_session)):
    "Função que retorna entidades do tipo Obra com paginação."

    offset = (p-1)*per_page
    statement = select(Obra).options(joinedload(Obra.responsavel)).offset(offset).limit(per_page)
    results = session.exec(statement).all()
    return results

@app.post('/obras', response_model = ObraResponse)
async def post_obras(obra: ObraPost, session = Depends(get_session)):
    "Função de cadastro de nova obra."

    responsavel = session.get(Responsavel, obra.id_responsavel)

    if responsavel is None or not responsavel.ativo:
        raise HTTPException(
            status_code=404,
            detail="Responsável não encontrado ou inativo.",
        )

    obra_db = Obra.model_validate(obra, from_attributes=True)
    obra_db.responsavel = responsavel  # Fazendo o lazy load da entidade para não dar erro depois
    session.add(obra_db)
    session.commit()
    session.refresh(obra_db)
    session.refresh(obra_db.responsavel)
    return obra_db

@app.put('/obra/{display_id}', response_model = ObraResponse)
async def atualizar_obra(display_id:str, obra_in: ObraPut, session = Depends(get_session)):
    "Função de atualização de nova obra."

    try:
        id = convert_display_to_numeric_id(display_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="ID de obra inválido.",
        ) from exc
    
    obra_db = session.get(Obra, id)

    if not obra_db:
        raise HTTPException(404, "Obra não encontrada.")

    dados_atualizar = obra_in.model_dump(exclude_unset = True)

    id_responsavel = dados_atualizar.get('id_responsavel', None)
    if id_responsavel:
        responsavel_db = session.get(Responsavel, id_responsavel)
        if not responsavel_db or not responsavel_db.ativo:
            raise HTTPException(400, "Responsável não existe ou está inativo.")

    for key, value in dados_atualizar.items():
        setattr(obra_db, key, value)

    session.add(obra_db)
    session.commit()
    session.refresh(obra_db)
    session.refresh(obra_db.responsavel)
    return obra_db

@app.delete('/obra/{display_id}')
async def delete_obra(display_id:str, session = Depends(get_session)):
    "Função de remoção de obra."

    try:
        id = convert_display_to_numeric_id(display_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="ID de obra inválido.",
        ) from exc
    
    obra_db = session.get(Obra, id)
    if not obra_db:
        raise HTTPException(404, "Obra não encontrada.")

    session.delete(obra_db)
    session.commit()
    return f"Obra {display_id} removida com sucesso."


################################################ Rotas da entidade Responsavel ################################################
@app.get('/responsaveis/', response_model = list[ResponsavelResponse])
async def get_responsaveis(ativo:bool = True, session = Depends(get_session)):
    "Função que retorna todas as entidades do tipo Responsavel. Opcionalmente tem um query parameter para retornar só os ativos, True por padrão."

    statement = select(Responsavel)
    if ativo:
        statement = statement.where(Responsavel.ativo == ativo)
    results = session.exec(statement).all()
    return results

@app.post('/responsaveis/', response_model = ResponsavelResponse)
async def post_responsaveis(responsavel: ResponsavelPost, session = Depends(get_session)):
    "Função que insere uma nova entidade do tipo responsável, e retorna o dado inserido no DB"
    responsavel_input = Responsavel.model_validate(responsavel, from_attributes=True)
    session.add(responsavel_input)
    session.commit()
    session.refresh(responsavel_input)
    return responsavel_input

@app.put('/responsavel/{id}', response_model = ResponsavelResponse)
async def atualizar_responsavel(id:int, 
                                responsavel_in: ResponsavelPut = None, 
                                session = Depends(get_session)):
    "Função para atualizar entidade do tipo responsável."
    responsavel_db = session.get(Responsavel, id)

    if not responsavel_db:
        raise HTTPException(404, "Entidade Responsavel não encontrada.")

    dados_atualizar = responsavel_in.model_dump(exclude_unset = True)
    for key, value in dados_atualizar.items():
        setattr(responsavel_db, key, value)

    session.add(responsavel_db)
    session.commit()
    session.refresh(responsavel_db)

    return responsavel_db

@app.delete('/responsavel/{id}')
async def deletar_responsavel(id:int, session = Depends(get_session)):
    "Função que faz soft delete de uma entidade Responsavel"
    statement = select(Responsavel).where(Responsavel.id == id).where(Responsavel.ativo == True)
    responsavel_db = session.exec(statement).first()

    if not responsavel_db:
        raise HTTPException(404, "Entidade Responsavel não encontrada.")

    responsavel_db.ativo = False
    session.add(responsavel_db)
    session.commit()
    return "Entidade removida com sucesso."

################################################ Rotas de teste ################################################
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/teste")
async def teste():
    "Função que retorna um objeto Obra com dados fictícios para teste de rota."
    return {'id': 'D-0001',
            'projeto': 'Reforma no banheiro do 1º andar',
            'id_responsavel': 120,
            'data_inicio': '2023-01-15',
            'data_fim': '2023-02-15',
            'status': 'Em andamento',
            'orcamento': 5000.00,
            'endereco': 'Rua das Flores, 123, Bairro Jardim, Cidade XYZ',
            'descricao': 'Reforma completa do banheiro, incluindo troca de azulejos, instalação de novos acessórios e pintura.',
            'contratante': 'Prefeitura Municipal de Cidade XYZ',
            'telefone_contratante': '(11) 1234-5678',
            'email_contratante': 'contato@prefeitura-cidadexyz.com.br',
            }

@app.get('/teste-param/{id}')
async def teste_param(id: str, orcamento:float = 5000.00):
    "Função que verifica query e path parameters e retorna um dicionário com os dados do projeto."
    return {'id': id,
            'projeto': 'Reforma no banheiro do 1º andar',
            'id_responsavel': 120,
            'data_inicio': '2023-01-15',
            'data_fim': '2023-02-15',
            'status': 'Em andamento',
            'orcamento': orcamento,
            'endereco': 'Rua das Flores, 123, Bairro Jardim, Cidade XYZ',
            'descricao': 'Reforma completa do banheiro, incluindo troca de azulejos, instalação de novos acessórios e pintura.',
            'contratante': 'Prefeitura Municipal de Cidade XYZ',
            'telefone_contratante': '(11) 1234-5678',
            'email_contratante': 'contato@prefeitura-cidadexyz.com.br',}

@app.get('/test-db')
async def test_db():
    try:
        test_db_connection()
        return {"message": "Conexão com o banco de dados bem-sucedida!"}
    except Exception as e:
        print(e)
        return {"message": "Falha na conexão com o banco de dados."}
