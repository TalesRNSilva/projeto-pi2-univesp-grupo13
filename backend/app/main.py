### Módulo que vai gerenciar as rotas e instanciar o APP
from db.db_conn import *
from fastapi import FastAPI

## Para rodar: 'uvicorn main:app --reload' na pasta /app/

app = FastAPI()

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