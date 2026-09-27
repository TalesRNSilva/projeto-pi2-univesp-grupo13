# Design Doc: Obral \- Gestão pra toda obra

### Especificação de Funcionalidades e Modelo de Dados

| Campo | Valor |
| :---- | :---- |
| Versão | 0.2 |
| Status | Validado |
| Última atualização | 27/09/2026 |

---

## 1\. Visão Geral

**Problema:** Fornecer um meio **seguro** e **prático** para gestão de dados a respeito de obras (serviços na construção civil) usando arquitetura cliente-servidor, com acesso via navegador. O objetivo, além da manutenção facilitada das informações a respeito de tais serviços, é permitir a fácil visualização dessas informações de modo a facilitar a gestão de empresas de pequeno porte.

**Usuário principal:** Francisco Chagas, dono da microempresa Chagas Empreendimentos e Construção Civil.

---

## 2\. Escopo

### 2.1 Incluído nesta versão

- CRUD de informações a respeito de obras via interface Web, usando API RESTful em Python com FastAPI e MySQL  
- Cadastro e remoção de pessoas responsáveis  
- Exportação de dados

### 2.2 Fora de escopo (por ora)

- Autenticação  
- Dashboard  
- Visualização de calendário

---

## 3\. Glossário

| Termo | Definição |
| :---- | :---- |
| **Obra** | Serviço prestado em construção civil, como construção de rede hidráulica ou elétrica; marcenaria; estrutura; piso; e afins.  |
| **Responsável** | Profissional que ficou responsável pela execução da obra, mesmo não sendo a única ou mesmo a principal mão de obra. |

---

## 4\. Modelo de Dados

### 4.1 Entidade: Obra

| Campo | Tipo | Obrigatório | Descrição / Regras |
| :---- | :---- | :---- | :---- |
| ID (PK) | String | Sim | Id alfanumérico **gerado pelo código** no momento do cadastro da obra, no formato ‘O-0001’, incremental. Por segurança, de O-9999 passar para O-10000 e assim por diante.  |
| Projeto | String | Sim | Nome da obra sendo feita (E.g. ‘Instalação Elétrica Casa’). Min 3, max 100 caracteres. |
| ID Responsável (FK) | Int | Talvez | Pessoa responsável pela obra. FK com entidade ‘responsável’. Entidade Responsável não pode ser hard-deleted; mas se for, anular o valor. |
| Data de início | Date | Sim | Data de início previsto (ou real) da Obra |
| Previsão de conclusão | Date | Sim | Data de conclusão prevista (ou real) da Obra. Não pode ser anterior à data de início |
| Status | Enum | Sim | Uma de quatro opções: Concluído, Em Andamento, Encerrado, Não Iniciado. Padrão de “Não Iniciado”. |
| Orçamento | Boolean | Não | Orçamento previsto (ou real) para a Obra. Não pode ser negativo. |
| Endereço | String | Não | Campo livre de endereço em que a Obra será realizada. Max 250 caracteres |
| Descrição | String | Não | Campo livre de descrição geral da Obra \- para observações mais detalhadas que não são contempladas nos outros campos. Max 500 caracteres |
| Contratante | String | Não | Nome completo da pessoa que contratou a obra. Min 3, max 100 caracteres |
| Telefone | String | Não | Telefone do contratante da Obra. Formato de telefone com DDD \- (XX) XXXXX-XXXX. 9 a 12 caracteres |
| E-mail Contratante | String | Não | E-mail do contratante da Obra. Validação básica de e-mail. Max 100 Caracteres. |
| Horário do cadastro | Timestamp | Sim | Timestamp em que a entidade foi criada. Gerado no momento da criação da entidade ou pelo código, ou pelo próprio DB. |
| Horário da última alteração | Timestamp | Sim | Timestamp em que a entidade foi alterada pela última vez. Quando a entidade é criada, deve ser a mesma hora da criação. Quando a entidade for alterada, o campo deve ser alterado automaticamente pelo código ou pelo próprio DB. |

### 4.2 Entidade: Responsável

| Campo | Tipo | Obrigatório | Descrição / Regras |
| :---- | :---- | :---- | :---- |
| ID (PK) | Int | Sim | ID único gerado no momento da inserção do objeto, incrementalmente, **pelo próprio DB** \- usar qualificador incremental do MySQL |
| Nome | String | Sim | Nome completo da pessoa responsável; min 3, max 100 caracteres. |
| Email | String | Não | Validação básica de email (@, domínio válido). Max 100 caracteres |
| Ativo | Boolean | Sim | Campo indicando se aquele responsável está ativo no sistema (i.e. funciona como soft delete). Padrão “TRUE”. |
| Horário do cadastro | Timestamp | Sim | Timestamp em que a entidade foi criada. Gerado no momento da criação da entidade ou pelo código, ou pelo próprio DB. |

### 4.3 Relacionamentos

- **Obra** ↔ **Responsável**: 1:N. Um responsável pode gerir várias obras, mas cada obra só tem um responsável.

>   
![][image1]  
figura 1 \- MER das entidades a nível lógico

---

## 5\. Funcionalidades

### 5.1 CRUD de Obras

**Descrição:** Cadastro, atualização, consulta e remoção de entidades do tipo **Obra** no database. Toda interação é feita via páginas da Web. A consulta traz uma visualização detalhada da entidade, com opções de edição e remoção. Cadastro é feito numa página à parte. Cadastro da entidade **Responsável** também é feito numa página à parte.

**Entidade(s) envolvida(s):** Obra, Responsável

**Campos do formulário / interação:** A maior parte dos campos são inputs de string padrão \- nenhum ID interno é exposto. Exceção são **Datas**, **Telefones**, **Email** e **Responsável** No caso do **Responsável**, apenas o nome é exibido. Cadastro da entidade **Responsável** é feito numa página à parte. Seguem algumas regras de formulários específicos:

* **Campos de data:** Seleção com calendário de data, com default para a data atual.  
* **Campo de telefone**: Máscara de DDD.  
* **Campo de responsável**: Seleção via nome do responsável em uma Dropdown Box. Somente entidades com `is_active = True` estão disponíveis pra seleção.  
* **Orçamento**: Máscara de R\$ XXX,XX, com no máximo dois decimais.  
* **Campo de Status**: Campo do tipo seleção exclusiva obrigatória, com escolha padrão “Não Iniciado”.

**Critérios de aceite:**

* Campos não nulos estão não nulos e regras de validação básicas como estipuladas no esquema do database \- e-mail e telefone têm que estar em formato válido. Orçamento não pode ser negativo, nem desviar do formato XXX,XX  
* A Obra **precisa** ter um responsável \- o responsável tem que ser um dos valores cadastrados. Permitir cadastro durante a inserção da própria obra.  
* Data de início não pode ser posterior à data de término  
* **Status** tem que ser um dos quatro valores permitidos

**Telas relacionadas:**  
	Cadastro de Obras; Visualização Geral

### 5.2 CRUD de Responsáveis

**Descrição**: Cadastro, atualização, consulta e remoção de entidades do tipo **Responsável** no database. A remoção é no modelo soft-delete através do campo `is_active`. O cadastro é feito numa página à parte. A atualização é feita na mesma página do cadastro \- ambas criam um pop-up na tela de responsáveis. 

**Entidade(s)** **envolvida(s)**: Responsável

**Campos do formulário / interação:** Campo de nome do responsável em destaque, com campos opcionais de email e telefone. Fluxo de adição, alteração e remoção deve ser bastante simplificado. Exclusão deve ser um soft-delete, alterando a flag `is_active` de `TRUE` para `FALSE`.   
	Como é esperado que a obra seja designada a um responsável, deve haver uma opção simples de criação de um Responsável durante a criação de uma obra \- uma janela replicando as visões de cadastro da tela de responsáveis deve ser o suficiente.

**Critérios de aceite**:

* Apenas o nome não deve ser nulo. Podem nomes e outros campos repetidos. O ID não pode ser inserido na requisição \- este é criado automaticamente pelo database quando da inserção, e deve ser retornado na requisição 200\.

**Telas relacionadas:**  
	Cadastro de responsáveis; Cadastro de Obras

### 5.3 Exportação de dados

**Descrição:** Os dados relacionados às Obras, tal como expostos na tela de visualização geral, devem ser fáceis de exportar para inserção em novos fluxos. A princípio, apenas formato **CSV**. Se a visualização em questão pode ser filtrada, deve haver opção para exportar com ou sem os filtros

**Entidade(s) envolvida(s)**: Obra, Responsável

**Campos do formulário / interação:** Botão simples de exportação nas telas relevantes, com janela de confirmação se necessário.

**Critérios de aceite**:

* O export deve ser abortado se os dados em questão estiverem vazios. Nunca gerar um export vazio.

**Telas relacionadas:**  
	Visualização geral; Dashboard

### 5.4 Dashboard de dados

**Descrição:** A confirmar o desenho

---

## 6\. Outline básico do Front

### 6.1 \- Componentes gerais (todas as telas):

* **Barra de navegação** \- Barra de navegação, com link para todas as telas, contendo o logotipo e o nome do projeto, apontando qual tela atualmente está ativa.  
* **Footer** \- Footer básico citando que se trata de um trabalho acadêmico da Univesp, opcionalmente com o nome dos integrantes.

### 6.2 \- Telas \- [Figma](https://www.figma.com/make/0IZkIYtjQz6O0x9cadUN74/Cadastro_Obras?p=f&fullscreen=1)

| Tela | Funcionalidade(s) relacionada(s) | Descrição breve | Endpoint previsto (back) | Path URL (front) |
| :---- | :---- | :---- | :---- | :---- |
| Visualização Geral (Obras) | CRUD de Obras Export de Dados | Visualização geral das entidades Obras, consolidando o número de obras total e por status em cartões no topo da tela. Deve suportar paginação (sugestão: 10 obras por página). Obras devem vir num formato de lista simples, trazendo ID, nome do projeto, nome do responsável, data de  previsão e status. Além disso, deve ser colapsável para mostrar detalhes da obra \- exibindo um botão de edição e outro de remoção no canto inferior direito. Botão de “nova obra” levando à mesma tela que a barra superior de navegação “Cadastrar” leva. Deve ter botão de “Exportar Dados” próximo ao topo, exportando ou toda entidade Obra com os mesmos detalhes da visualização, ou apenas as filtradas. | /obras/ /obra/\<id\>/alterar /obra/\<id\>/excluir /obras/download | /home |
| Cadastro de Obras (Cadastrar) | CRUD de Obras, CRUD de Responsáveis | Tela que realiza o cadastro de cada obra. O campo é seccionado pelo tipo de informação (Obra / Detalhes Adicionais / Contratante). Tela simples, aplicando a máscara e o tipo de validação descrito em cada campo. | /obras/cadastrar | /cadastro |
| Responsáveis (Responsáveis) | CRUD de Responsáveis | Tela que realiza o cadastro da entidade Responsável, com um formulário simples para a adição de novas entidades. As entidades existentes são então exibidas \- com paginação \-, com um simples botão de remoção e edição. A edição deve abrir um popup de um formulário com campos editáveis, e a remoção deve abrir uma janela de confirmação. Opcionalmente, trazer estatísticas resumidas por responsável (número de obras, tempo de cadastro). | /responsaveis /responsavel/\<id\> | /responsaveis |

---

## 7\. Pontes com outros documentos

| Documento | O que ele decide | Link |
| :---- | :---- | :---- |
| Design System | Cores, fontes, logotipo, componentes visuais | A criar |
| Doc de Implementação Back-End | Rotas, schemas de request/response, payloads | A criar |

---

## 8\. Questões em aberto

| Questão | Status | Descrição | Decisão |
| :---- | :---- | :---- | :---- |
| Adicionar autenticação? | Em aberto | Autenticação básica para fins de proteção de dados. Criação de contas seria gerenciada por uma conta master \- cujas credenciais são registradas na primeira ativação do programa \-, e nunca de forma independente. |  |
| Desenho específico do dashboard | Em aberto | Que tipo de visualização trazer na página de dashboard, com base nos atributos cadastrados. |  |
| Adicionar visualização de calendário? | Em aberto | Calendário mostrando uma visão simplificada das obras baseado no dia do calendário \- similar ao Google Calendar. Clicar num dia com obras deveria produzir uma visão detalhada apenas daquelas obras. |  |
| Adicionar filtros na tela de visualização geral? | Em aberto | Permitir filtragem das Obras exibidas na tela de Visualização Geral. Os campos de filtragem seriam alguns campos mais robustos da entidade Obras, como nome do responsável, status, orçamento e datas |  |

---

## 9\. Changelog

| Data | Autor | Alteração |
| :---- | :---- | :---- |
| 18/09/2026 | Tales Silva | Criação do documento |
