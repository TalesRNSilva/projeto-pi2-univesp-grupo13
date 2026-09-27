/** Dados locais usados apenas para a demonstração do protótipo. */
const obrasDemo = [
  {
    id: "#001",
    projeto: "Casa Elétrica",
    responsavel: "Francisco Chagas",
    status: "Concluído",
    inicio: "01/06/2026",
    previsao: "01/08/2026",
    orcamento: "R$ 15.000,00",
    endereco: "Rua das Flores, 120 - Centro",
    contratante: "Antônio Lima",
    telefone: "(85) 99999-0001",
    email: "antonio@email.com",
    descricao: "Instalação elétrica completa",
  },
  {
    id: "#002",
    projeto: "Casa Construção",
    responsavel: "Francisco Chagas",
    status: "Em andamento",
    inicio: "15/06/2026",
    previsao: "26/09/2026",
    orcamento: "R$ 48.500,00",
    endereco: "Av. Central, 450 - Aldeota",
    contratante: "Mariana Costa",
    telefone: "(85) 98888-0202",
    email: "mariana@email.com",
    descricao: "Construção residencial em fase de acabamento.",
  },
  {
    id: "#003",
    projeto: "Muro",
    responsavel: "Francisco Chagas",
    status: "Encerrado",
    inicio: "10/08/2026",
    previsao: "15/10/2026",
    orcamento: "R$ 8.200,00",
    endereco: "Rua do Sol, 85 - Meireles",
    contratante: "Carlos Mendes",
    telefone: "(85) 97777-0303",
    email: "carlos@email.com",
    descricao: "Execução de muro perimetral.",
  },
  {
    id: "#004",
    projeto: "Revestimento Cozinha",
    responsavel: "Maria Santos",
    status: "Em andamento",
    inicio: "20/08/2026",
    previsao: "20/11/2026",
    orcamento: "R$ 6.750,00",
    endereco: "Rua das Acácias, 310 - Papicu",
    contratante: "Luiza Ferreira",
    telefone: "(85) 96666-0404",
    email: "luiza@email.com",
    descricao: "Assentamento de revestimento e rejunte.",
  },
  {
    id: "#005",
    projeto: "Piso Casa",
    responsavel: "João Oliveira",
    status: "Em andamento",
    inicio: "02/09/2026",
    previsao: "29/12/2026",
    orcamento: "R$ 12.300,00",
    endereco: "Rua das Palmeiras, 72 - Cocó",
    contratante: "Rafael Nunes",
    telefone: "(85) 95555-0505",
    email: "rafael@email.com",
    descricao: "Troca do piso das áreas internas.",
  },
];

const listaObras = document.getElementById("lista-obras");
const paginacaoObras = document.getElementById("paginacao-obras");
const obrasPorPagina = 10;
let paginaAtual = 1;

function classeStatus(status) {
  return {
    "Concluído": "concluido",
    "Em andamento": "andamento",
    "Encerrado": "encerrado",
    "Não Iniciado": "nao-iniciado",
  }[status] || "nao-iniciado";
}

function atualizarResumo() {
  document.getElementById("total-obras").textContent = obrasDemo.length;
  document.getElementById("total-concluidas").textContent = obrasDemo.filter((obra) => obra.status === "Concluído").length;
  document.getElementById("total-andamento").textContent = obrasDemo.filter((obra) => obra.status === "Em andamento").length;
  document.getElementById("total-encerradas").textContent = obrasDemo.filter((obra) => obra.status === "Encerrado").length;
}

function campoDetalhe(rotulo, valor) {
  return `<dl class="detail-field"><dt>${rotulo}</dt><dd>${valor}</dd></dl>`;
}

function renderizarObras() {
  atualizarResumo();
  const totalPaginas = Math.max(1, Math.ceil(obrasDemo.length / obrasPorPagina));
  const inicio = (paginaAtual - 1) * obrasPorPagina;
  const obrasVisiveis = obrasDemo.slice(inicio, inicio + obrasPorPagina);

  listaObras.innerHTML = obrasVisiveis.map((obra) => `
    <article class="project-card" data-id="${obra.id}">
      <button class="project-summary" type="button" aria-expanded="false">
        <span class="project-id">${obra.id}</span>
        <span class="project-name">${obra.projeto}</span>
        <span class="project-owner">${obra.responsavel}</span>
        <span class="project-date">Prev: ${obra.previsao}</span>
        <span class="status-badge status-${classeStatus(obra.status)}">${obra.status}</span>
        <span class="expand-indicator" aria-hidden="true"></span>
      </button>
      <div class="project-details">
        <div class="detail-columns">
          <section class="detail-group" aria-label="Projeto">
            <h2>Projeto</h2>
            ${campoDetalhe("ID", obra.id)}
            ${campoDetalhe("Projeto", obra.projeto)}
            ${campoDetalhe("Responsável", obra.responsavel)}
            ${campoDetalhe("Status", `<span class="status-badge status-${classeStatus(obra.status)}">${obra.status}</span>`)}
          </section>
          <section class="detail-group" aria-label="Datas e orçamento">
            <h2>Datas e Orçamento</h2>
            ${campoDetalhe("Data de Início", obra.inicio)}
            ${campoDetalhe("Previsão", obra.previsao)}
            ${campoDetalhe("Orçamento", obra.orcamento)}
            ${campoDetalhe("Endereço", obra.endereco)}
          </section>
          <section class="detail-group" aria-label="Contratante">
            <h2>Contratante</h2>
            ${campoDetalhe("Nome", obra.contratante)}
            ${campoDetalhe("Telefone", obra.telefone)}
            ${campoDetalhe("E-mail", obra.email)}
          </section>
        </div>
        <section class="detail-group details-description" aria-label="Detalhes adicionais">
          <h2>Detalhes Adicionais</h2>
          <p>${obra.descricao}</p>
        </section>
        <div class="detail-actions">
          <button class="button button-danger" type="button" data-action="excluir">Excluir obra</button>
          <button class="button button-primary" type="button" data-action="editar">Editar</button>
        </div>
      </div>
    </article>
  `).join("");

  document.getElementById("list-caption").textContent = `${obrasDemo.length} registros · clique em uma obra para expandir os detalhes`;
  paginacaoObras.hidden = totalPaginas === 1;
  paginacaoObras.innerHTML = totalPaginas > 1
    ? `<button type="button" data-page="${paginaAtual - 1}" aria-label="Página anterior" ${paginaAtual === 1 ? "disabled" : ""}>‹</button><span>Página ${paginaAtual} de ${totalPaginas}</span><button type="button" data-page="${paginaAtual + 1}" aria-label="Próxima página" ${paginaAtual === totalPaginas ? "disabled" : ""}>›</button>`
    : "";
}

function exportarCsv() {
  if (obrasDemo.length === 0) {
    window.alert("Não há obras para exportar.");
    return;
  }

  const colunas = ["ID", "Projeto", "Responsável", "Status", "Data de início", "Previsão", "Orçamento", "Endereço", "Contratante", "Telefone", "E-mail", "Descrição"];
  const valores = obrasDemo.map((obra) => [obra.id, obra.projeto, obra.responsavel, obra.status, obra.inicio, obra.previsao, obra.orcamento, obra.endereco, obra.contratante, obra.telefone, obra.email, obra.descricao]);
  const csv = [colunas, ...valores]
    .map((linha) => linha.map((valor) => `"${String(valor).replaceAll('"', '""')}"`).join(";"))
    .join("\r\n");
  const arquivo = new Blob([`\uFEFF${csv}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(arquivo);
  const link = document.createElement("a");
  link.href = url;
  link.download = "obral-obras.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

listaObras.addEventListener("click", (evento) => {
  const botaoAcao = evento.target.closest("[data-action]");
  const cartao = evento.target.closest(".project-card");

  if (!cartao) return;

  if (botaoAcao?.dataset.action === "excluir") {
    if (window.confirm("Deseja excluir esta obra da demonstração?")) {
      const indice = obrasDemo.findIndex((obra) => obra.id === cartao.dataset.id);
      obrasDemo.splice(indice, 1);
      paginaAtual = Math.min(paginaAtual, Math.max(1, Math.ceil(obrasDemo.length / obrasPorPagina)));
      renderizarObras();
    }
    return;
  }

  if (botaoAcao?.dataset.action === "editar") {
    window.alert("A edição não está conectada nesta demonstração.");
    return;
  }

  const resumo = evento.target.closest(".project-summary");
  if (resumo) {
    const aberto = cartao.classList.toggle("is-open");
    resumo.setAttribute("aria-expanded", String(aberto));
  }
});

paginacaoObras.addEventListener("click", (evento) => {
  const botao = evento.target.closest("[data-page]");
  if (!botao || botao.disabled) return;
  paginaAtual = Number(botao.dataset.page);
  renderizarObras();
});

document.getElementById("exportar-obras").addEventListener("click", exportarCsv);
renderizarObras();
