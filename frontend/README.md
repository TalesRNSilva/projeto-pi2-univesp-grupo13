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
js/home.js             # lógica específica da tela de Visualização Geral
js/cadastro.js         # lógica específica da tela de Cadastro
js/responsaveis.js     # lógica específica da tela de Responsáveis
assets/                # imagens, logotipo etc.
```

## Conectando com o back-end

Toda a comunicação com a API passa por `js/api.js`. Ao publicar o back-end,
atualize a constante `BASE_URL` nesse arquivo com o endereço público da API.
É a única mudança necessária pro front encontrar o back em produção.

## Publicando (deploy)

Em serviços como Netlify, Vercel ou GitHub Pages, configure:
- **Base / root directory:** `frontend`
- **Build command:** (deixe em branco — não há etapa de build)
- **Publish directory:** `frontend` (ou `.`, relativo à base directory)
