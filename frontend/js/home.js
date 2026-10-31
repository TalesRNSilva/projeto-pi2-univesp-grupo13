const listaObras = document.getElementById("lista-obras");
const paginacaoObras = document.getElementById("paginacao-obras");
const obrasPorPagina = 10;
let paginaAtual = 1;
let totalPaginas = 1;
const filtrosObras = document.getElementById("filtros-obras");
let campoOrdenacao = "ultima_atualizacao";
let direcaoOrdenacao = "desc";

function classeStatus(status) {
  return {
    "Concluído": "concluido",
    "Em andamento": "andamento",
    "Encerrado": "encerrado",
    "Não iniciado": "nao-iniciado",
    "Não Iniciado": "nao-iniciado",
  }[status] || "nao-iniciado";
}

function escapeHtml(valor) {
  return String(valor ?? "").replace(/[&<>"']/g, (caractere) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
  }[caractere]));
}

function dataFormatada(valor) {
  if (!valor) return "—";
  return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(new Date(`${valor}T00:00:00Z`));
}

function moedaFormatada(valor) {
  if (valor === null || valor === undefined || valor === "") return "—";
  return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(valor));
}

function campoDetalhe(rotulo, valor) {
  return `<dl class="detail-field"><dt>${rotulo}</dt><dd>${valor || "—"}</dd></dl>`;
}

function atualizarResumo(obras, total) {
  document.getElementById("total-obras").textContent = total;
  document.getElementById("total-concluidas").textContent = obras.filter((obra) => obra.status === "Concluído").length;
  document.getElementById("total-andamento").textContent = obras.filter((obra) => obra.status === "Em andamento").length;
  document.getElementById("total-encerradas").textContent = obras.filter((obra) => obra.status === "Encerrado").length;
}

function renderizar(obras, total) {
  atualizarResumo(obras, total);
  listaObras.innerHTML = obras.map((obra) => {
    const responsavel = obra.responsavel?.nome || "Sem responsável";
    return `<article class="project-card" data-id="${escapeHtml(obra.display_id)}">
      <button class="project-summary" type="button" aria-expanded="false">
        <span class="project-id">${escapeHtml(obra.display_id)}</span>
        <span class="project-name">${escapeHtml(obra.projeto)}</span>
        <span class="project-owner">${escapeHtml(responsavel)}</span>
        <span class="project-date">Prev: ${dataFormatada(obra.data_conclusao)}</span>
        <span class="status-badge status-${classeStatus(obra.status)}">${escapeHtml(obra.status)}</span>
        <span class="expand-indicator" aria-hidden="true"></span>
      </button>
      <div class="project-details">
        <div class="detail-columns">
          <section class="detail-group"><h2>Projeto</h2>
            ${campoDetalhe("ID", escapeHtml(obra.display_id))}
            ${campoDetalhe("Projeto", escapeHtml(obra.projeto))}
            ${campoDetalhe("Responsável", escapeHtml(responsavel))}
            ${campoDetalhe("Status", `<span class="status-badge status-${classeStatus(obra.status)}">${escapeHtml(obra.status)}</span>`)}
          </section>
          <section class="detail-group"><h2>Datas e Orçamento</h2>
            ${campoDetalhe("Data de início", dataFormatada(obra.data_inicio))}
            ${campoDetalhe("Previsão", dataFormatada(obra.data_conclusao))}
            ${campoDetalhe("Orçamento", moedaFormatada(obra.orcamento))}
            ${campoDetalhe("Endereço", escapeHtml(obra.endereco))}
          </section>
          <section class="detail-group"><h2>Contratante</h2>
            ${campoDetalhe("Nome", escapeHtml(obra.contratante))}
            ${campoDetalhe("Telefone", escapeHtml(obra.telefone))}
            ${campoDetalhe("E-mail", escapeHtml(obra.email_contratante))}
          </section>
        </div>
        <section class="detail-group details-description"><h2>Detalhes adicionais</h2><p>${escapeHtml(obra.descricao) || "—"}</p></section>
        <div class="detail-actions">
          <button class="button button-danger" type="button" data-action="excluir">Excluir obra</button>
          <button class="button button-primary" type="button" data-action="editar">Editar</button>
        </div>
      </div>
    </article>`;
  }).join("") || '<p class="empty-state">Nenhuma obra cadastrada.</p>';
  document.getElementById("list-caption").textContent = `${total} registros · clique em uma obra para expandir os detalhes`;
  paginacaoObras.hidden = totalPaginas <= 1;
  paginacaoObras.innerHTML = `<button type="button" data-page="${paginaAtual - 1}" ${paginaAtual === 1 ? "disabled" : ""}>‹</button>
    <span>Página ${paginaAtual} de ${totalPaginas}</span>
    <button type="button" data-page="${paginaAtual + 1}" ${paginaAtual === totalPaginas ? "disabled" : ""}>›</button>`;
}

async function carregarObras() {
  listaObras.innerHTML = '<p class="empty-state">Carregando obras...</p>';
  try {
    const parametros = new URLSearchParams({
      p: paginaAtual,
      per_page: obrasPorPagina,
      sort_by: campoOrdenacao,
      sort_order: direcaoOrdenacao,
    });
    filtrosObras.querySelectorAll("[data-status].is-active").forEach((pill) => {
      parametros.append("status", pill.dataset.status);
    });
    const resposta = await apiGet(`/obras?${parametros}`);
    const obras = resposta.obras || resposta.data || resposta.items || [];
    totalPaginas = resposta.total_pages || 1;
    paginaAtual = resposta.current_page || paginaAtual;
    renderizar(obras, resposta.total_items ?? obras.length);
  } catch (erro) {
    listaObras.innerHTML = `<p class="error-message">${escapeHtml(erro.message)}</p>`;
  }

}

filtrosObras.addEventListener("click", (evento) => {
  const sortPill = evento.target.closest("[data-sort]");
  const statusPill = evento.target.closest("[data-status]");

  if (sortPill) {
    if (sortPill.dataset.sort === campoOrdenacao) {
      direcaoOrdenacao = direcaoOrdenacao === "desc" ? "asc" : "desc";
    } else {
      campoOrdenacao = sortPill.dataset.sort;
    }
    filtrosObras.querySelectorAll("[data-sort]").forEach((pill) => {
      const active = pill.dataset.sort === campoOrdenacao;
      pill.classList.toggle("is-active", active);
      pill.setAttribute("aria-pressed", String(active));
      const arrow = pill.querySelector(".sort-arrow");
      if (arrow) arrow.textContent = active ? (direcaoOrdenacao === "desc" ? "↓" : "↑") : "";
    });
    paginaAtual = 1;
    carregarObras();
    return;
  }

  if (statusPill) {
    const active = statusPill.classList.toggle("is-active");
    statusPill.setAttribute("aria-pressed", String(active));
    paginaAtual = 1;
    carregarObras();
  }
});

document.getElementById("limpar-filtros").addEventListener("click", () => {
  campoOrdenacao = "ultima_atualizacao";
  direcaoOrdenacao = "desc";
  filtrosObras.querySelectorAll("[data-sort]").forEach((pill) => {
    const active = pill.dataset.sort === campoOrdenacao;
    pill.classList.toggle("is-active", active);
    pill.setAttribute("aria-pressed", String(active));
    const arrow = pill.querySelector(".sort-arrow");
    if (arrow) arrow.textContent = active ? "↓" : "";
  });
  filtrosObras.querySelectorAll("[data-status]").forEach((pill) => {
    pill.classList.remove("is-active");
    pill.setAttribute("aria-pressed", "false");
  });
  paginaAtual = 1;
  carregarObras();
});

listaObras.addEventListener("click", async (evento) => {
  const cartao = evento.target.closest(".project-card");
  if (!cartao) return;
  const acao = evento.target.closest("[data-action]")?.dataset.action;
  if (acao === "editar") {
    window.location.href = `cadastro.html?id=${encodeURIComponent(cartao.dataset.id)}`;
    return;
  }
  if (acao === "excluir" && window.confirm("Deseja excluir esta obra?")) {
    try { await apiDelete(`/obra/${cartao.dataset.id}`); await carregarObras(); }
    catch (erro) { window.alert(erro.message); }
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
  carregarObras();
});

document.getElementById("exportar-obras").addEventListener("click", async () => {
  try {
    const blob = await apiDownload("/obras/download");
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url; link.download = "obral-obras.csv"; link.click();
    URL.revokeObjectURL(url);
  } catch (erro) { window.alert(erro.message); }
});

carregarObras();
