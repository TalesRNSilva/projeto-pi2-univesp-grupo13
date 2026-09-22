# Backend — Obral API

API em FastAPI que expõe as entidades **Obra** e **Responsável**, com dados
armazenados em MySQL (instância na nuvem — a string de conexão vem do `.env`).

## Rodando localmente

1. Crie um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e preencha com os dados do banco MySQL:
   ```
   cp .env.example .env
   ```
4. Rode o servidor:
   ```
   uvicorn app.main:app --reload
   ```
5. Acesse a documentação automática (gerada sozinha pelo FastAPI) em
   http://localhost:8000/docs — dá pra testar cada endpoint por ali mesmo,
   sem precisar do front.

## Estrutura

```
app/
├── main.py        # cria o app e conecta as rotas
├── config.py      # lê o .env
├── database.py    # conexão com o MySQL
├── modelos/        # tabelas do banco (SQLAlchemy) — uma por entidade
└── rotas/       # os endpoints em si, um arquivo por entidade
```

Os endpoints hoje retornam dados de exemplo (stub) — procure por `# TODO`
em `app/routers/` pra saber onde entra a lógica real de banco.

## Adicionalmente

Não criei, mas podemos criar uma pasta com schemas em pydantic ou outro módulo
pra gerenciar a validação de dados entre front e back. Enquanto `modelos/` gerencia
os modelos de dados a nível de integração back e DB, `schemas/` poderia gerenciar
o contrato front e back-end - tal como garantir que os dados estão vindo no formato
certo na requisição, e estabelecendo um padrão único de resposta para cada endpoint.

## Nota sobre as rotas

O Design Doc (seção 6.2) lista os endpoints usando ora "obra" ora "obras"
no singular/plural (ex.: `/obras/` e `/obra/<id>/alterar`). Neste código,
padronizei tudo no plural (`/obras/...`) por consistência REST — ajustem o
Design Doc ou o código se preferirem manter o singular nas rotas de detalhe.

## Publicando (deploy)

Em serviços como Render ou Railway, configure:
- **Root directory:** `backend`
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Configure a variável de ambiente `DATABASE_URL` no painel do serviço —
nunca commitem o `.env` real (ele já está no `.gitignore`).
