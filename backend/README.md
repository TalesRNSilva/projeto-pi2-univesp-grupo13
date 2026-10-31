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

## Deploy no Render

O arquivo `render.yaml` na raiz do repositório já define um Web Service com
`backend` como diretório raiz. Ao usar Blueprint, configure no Render as
variáveis `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_USER`,
`DATABASE_PASSWORD`, `DATABASE_NAME` e `DATABASE_SSL_CA`. Para o certificado
que já está no repositório, use `ca.pem` como valor de `DATABASE_SSL_CA`.

Se criar o serviço pelo Dashboard, use:

- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/`

Nunca coloque senha ou o conteúdo do certificado em um arquivo versionado.
Depois do deploy, teste `/`, `/docs` e `/obras` usando a URL `onrender.com`.

## Estrutura

```
app/
├── main.py        # cria o app e conecta as rotas
├── config.py      # lê o .env
├── database.py    # conexão com o MySQL
├── modelos/        # tabelas do banco (SQLAlchemy) — uma por entidade
└── rotas/       # os endpoints em si, um arquivo por entidade
```

`GET /obras` aceita `p`, `per_page`, `sort_by`, `sort_order` e `status`, e
retorna `{ obras, current_page, total_pages, total_items }`. A ordenação
padrão é por `ultima_atualizacao` descendente. Os valores aceitos em
`sort_by` são `id`, `ultima_atualizacao` e `data_conclusao`; em `sort_order`,
`asc` e `desc`. `status` pode ser repetido para combinar os quatro valores
do enum de obras (por exemplo, `status=Concluído&status=Em%20andamento`).
`GET /obras/download` retorna todas as obras como um arquivo CSV UTF-8. O
download responde 404 quando não há obras.

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

Configure as variáveis de conexão descritas acima no painel do serviço —
nunca commite o `.env` real (ele já está no `.gitignore`).
