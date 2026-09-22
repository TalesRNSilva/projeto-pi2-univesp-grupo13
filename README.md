# Obral — Gestão pra toda obra

## O que é

Aplicação web cliente-servidor para o registro e acompanhamento de serviços
prestados em obras de construção civil (instalação elétrica, hidráulica,
alvenaria, marcenaria etc.), pensada para prestadores de pequeno porte que
hoje fazem esse controle de forma manual/informal.

Projeto acadêmico (Univesp).

## Arquitetura

Arquitetura cliente-servidor clássica: front-end estático consome uma API
RESTful, que por sua vez fala com um banco de dados relacional hospedado na
nuvem.

```
[ Navegador ]  --HTTP/JSON-->  [ API FastAPI ]  --SQL-->  [ MySQL (nuvem) ]
                                  backend/
   frontend/
```

- **Front-end:** HTML, CSS e JavaScript puro, sem framework (Bootstrap é
  opcional, só para estilo). Protótipos visuais feitos no Figma.
- **Back-end:** Python com FastAPI, expondo uma API REST.
- **Banco de dados:** MySQL, instanciado em um provedor de nuvem.

## Estrutura do repositório

Monorepo com duas metades independentes, cada uma publicável em um serviço
de hospedagem diferente:

```
obral/
├── backend/     # API em FastAPI + conexão com o MySQL
└── frontend/    # HTML/CSS/JS puro, uma página por tela
```

## Entidades principais

- **Obra** — um serviço prestado em construção civil. Guarda dados de
  cronograma (início/previsão de conclusão), status, orçamento, endereço e
  dados do contratante.
- **Responsável** — profissional encarregado da execução de uma obra.

Relação: um Responsável pode estar associado a várias Obras (1:N).

> O modelo de dados completo, com todos os campos, tipos e regras de
> validação, vive no Design Doc (seção 4) — este README não duplica isso de
> propósito, pra não haver duas fontes divergentes.

## Funcionalidades (escopo atual)

**Incluído nesta versão:**
- CRUD de Obras via interface Web
- Cadastro e remoção (soft-delete) de Responsáveis
- Exportação de dados em CSV

**Fora de escopo por ora:**
- Autenticação
- Dashboard
- Visualização em calendário

(ver seção 2 do Design Doc para o raciocínio por trás dessas escolhas)

## Documentação relacionada

- **Design Doc** — especificação de funcionalidades e modelo de dados;
  fonte da verdade do projeto.
- **Design System** — decisões de front-end (cores, fontes, logotipo) — a criar.
- **Doc de Implementação Back-End** — rotas, schemas de request/response — a criar.

## Status

Projeto em desenvolvimento inicial. A estrutura de pastas está sendo
montada; o ambiente de execução (dependências, variáveis de ambiente) ainda
será documentado à medida que os arquivos forem inicializados.