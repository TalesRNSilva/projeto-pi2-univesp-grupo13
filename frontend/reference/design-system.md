# Design System — Obral

Este documento consolida as decisões visuais já presentes nos protótipos do
Figma e no logotipo, para servir de referência única na implementação do
front-end. Ele é o "Documento de Design System" citado na seção 7 do Design
Doc.

## Logotipo

A definir

## Paleta de cores

| Token | Hex | Onde aparece nos protótipos |
|---|---|---|
| `--color-navy` | `#183054` | Navbar, cabeçalhos de seção do formulário, botões primários ("Salvar Obra", "+ Nova Obra", "Cadastrar"), avatares de responsável, texto do logotipo |
| `--color-teal` | `#18A0B0` | Anel do logotipo e tagline — **cor de marca**, hoje não usada em nenhum componente de UI além do logo |
| `--color-info` | `#00A8D8` | Badge/pill de status "Em andamento" |
| `--color-success` | `#5EB82E` | Badge de status "Concluído" |
| `--color-warning` | `#F0A020` | Badge de status "Encerrado" |
| `--color-bg` | `#F0F0F0` | Fundo geral da página |
| `--color-surface` | `#FFFFFF` | Cards, formulários, tabela |
| `--color-text` | `#242424` | Texto padrão do corpo |
| `--color-text-muted` | `#84909C` | Textos secundários (placeholders, legendas) |

## Tipografia

- Títulos de página / nome do produto: **bold**
- Cabeçalhos de seção do formulário (ex.: "IDENTIFICAÇÃO DO PROJETO"): bold,
  tamanho pequeno, letras espaçadas, caixa alta
- Labels de campo e corpo de texto: regular
- Botões: bold/semibold

```css
font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
```

## Componentes principais

- **Navbar** — fundo `--color-navy`, logotipo + nome do produto à esquerda,
  links de navegação à direita, link ativo destacado (fundo levemente mais
  claro ou sublinhado)
- **Botão primário** — fundo `--color-navy`, texto branco, cantos
  arredondados (~6–8px)
- **Botão secundário/cancelar** — fundo `--color-bg`, borda sutil, texto
  escuro
- **Badge/pill de status** — fundo sólido (`info`/`success`/`warning`),
  texto branco, cantos bem arredondados (pill)
- **Card de estatística** (topo da Visualização Geral) — fundo branco,
  número grande colorido conforme o status, label pequeno cinza abaixo
- **Cabeçalho de seção de formulário** — barra sólida `--color-navy` com
  texto branco em caixa alta, usada para seccionar o formulário de Obra em
  "Identificação do Projeto" / "Detalhes Adicionais" / "Informações do
  Contratante"
- **Avatar circular** (tela de Responsáveis) — círculo `--color-navy` com a
  inicial do nome em branco
- **Tabela** — cabeçalho `--color-navy` com texto branco, linhas alternando
  fundo branco/cinza claríssimo (zebra striping)

## Variáveis prontas para `frontend/css/styles.css`

```css
:root {
  /* cores de marca */
  --color-navy: #183054;
  --color-teal: #18A0B0;

  /* cores de status */
  --color-info: #00A8D8;
  --color-success: #5EB82E;
  --color-warning: #F0A020;

  /* neutros */
  --color-bg: #F0F0F0;
  --color-surface: #FFFFFF;
  --color-text: #242424;
  --color-text-muted: #84909C;

  /* tipografia */
  --font-base: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;

  /* espaçamento (escala de 4px, convenção — não medida a partir do print) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;

  /* raio de borda */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-pill: 999px;
}
```
