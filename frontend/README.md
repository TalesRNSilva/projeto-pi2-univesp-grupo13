# Frontend — Obral

Interface Web em HTML, CSS e JavaScript puro (sem framework de build).

## Rodando localmente

Não precisa de instalação. Basta abrir `index.html` no navegador, ou usar
uma extensão tipo "Live Server" (VSCode) para recarregar automaticamente a
cada alteração.

## Estrutura

```
index.html           # Visualização Geral (/home)
cadastro.html         # Cadastro de Obras (/cadastro)
responsaveis.html     # Cadastro de Responsáveis (/responsaveis)
css/styles.css         # estilos compartilhados por todas as telas
js/api.js              # configuração da URL do back-end + funções de requisição
js/home.js             # listagem paginada, edição, remoção e exportação
js/cadastro.js         # criação/edição de obras e cadastro rápido de responsável
js/responsaveis.js     # cadastro, edição e remoção (soft delete)
assets/                # imagens, logotipo etc.
```

## Conectando com o back-end

Toda a comunicação com a API passa por `js/api.js`. Ao publicar o back-end,
atualize a constante `BASE_URL` nesse arquivo com o endereço público da API.
É a única mudança necessária pro front encontrar o back em produção.

## Publicando no GitHub Pages

O workflow [`../.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml)
publica automaticamente o conteúdo desta pasta quando há um push na branch
`main`.

No GitHub, abra **Settings → Pages** e selecione **GitHub Actions** como
origem do deploy. Depois, faça push para `main` e acompanhe a execução na
aba **Actions**. A URL terá este formato:

```text
https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO/
```

Antes do primeiro deploy, confirme em [`js/api.js`](js/api.js) que `BASE_URL`
é a URL pública do backend no Render, sem uma barra final:

```javascript
const BASE_URL = "https://seu-backend.onrender.com";
```

O backend precisa permitir a origem do GitHub Pages via CORS. Enquanto
`allow_origins=["*"]` estiver configurado, isso já estará permitido. Para
produção, substitua o curinga pela URL exata do site publicado.

Como o frontend é HTML, CSS e JavaScript puro, não há build ou instalação de
dependências. O workflow envia diretamente `frontend` como artefato do Pages.
