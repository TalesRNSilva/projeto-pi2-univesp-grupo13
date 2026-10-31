const lista = document.getElementById("lista-responsaveis");
const mensagem = document.getElementById("mensagem-responsaveis");
const modal = document.getElementById("modal-edicao");
const formCadastro = document.getElementById("form-responsavel");
const formEdicao = document.getElementById("form-edicao");

function mostrarMensagem(texto, erro = false) {
  mensagem.textContent = texto;
  mensagem.className = `form-message ${erro ? "is-error" : "is-success"}`;
}

async function carregarResponsaveis() {
  try {
    const dados = await apiGet("/responsaveis/?ativo=true");
    lista.innerHTML = dados.map((item) => `<article class="responsavel-card"><span class="avatar">${item.nome.charAt(0).toUpperCase()}</span><div><strong>${item.nome}</strong><small>${item.email || "Sem e-mail"}</small></div><div class="card-actions"><button class="button button-secondary" data-edit="${item.id}">Editar</button><button class="button button-danger" data-delete="${item.id}">Remover</button></div></article>`).join("") || "<p>Nenhum responsável ativo cadastrado.</p>";
  } catch (erro) { lista.textContent = erro.message; }
}

formCadastro.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  try { await apiPost("/responsaveis/", Object.fromEntries(new FormData(formCadastro))); formCadastro.reset(); mostrarMensagem("Responsável cadastrado."); carregarResponsaveis(); }
  catch (erro) { mostrarMensagem(erro.message, true); }
});

lista.addEventListener("click", async (evento) => {
  const editar = evento.target.closest("[data-edit]");
  const remover = evento.target.closest("[data-delete]");
  if (editar) {
    try {
      const responsavel = (await apiGet("/responsaveis/?ativo=true")).find((item) => item.id === Number(editar.dataset.edit));
      formEdicao.elements.id.value = responsavel.id; formEdicao.elements.nome.value = responsavel.nome; formEdicao.elements.email.value = responsavel.email || "";
      modal.showModal();
    } catch (erro) { mostrarMensagem(erro.message, true); }
  } else if (remover && window.confirm("Deseja remover este responsável?")) {
    try { await apiDelete(`/responsavel/${remover.dataset.delete}`); carregarResponsaveis(); } catch (erro) { mostrarMensagem(erro.message, true); }
  }
});

formEdicao.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formEdicao)); const id = dados.id; delete dados.id;
  try { await apiPut(`/responsavel/${id}`, dados); modal.close(); carregarResponsaveis(); } catch (erro) { window.alert(erro.message); }
});

carregarResponsaveis();
