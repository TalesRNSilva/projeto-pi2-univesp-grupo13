const formObra = document.getElementById("form-obra");
const selectResponsavel = document.getElementById("responsavel");
const modalResponsavel = document.getElementById("modal-responsavel");
const obraId = new URLSearchParams(window.location.search).get("id");

function mostrarMensagem(texto, erro = false) {
  const elemento = document.getElementById("mensagem-form");
  elemento.textContent = texto;
  elemento.className = `form-message ${erro ? "is-error" : "is-success"}`;
}

async function carregarResponsaveis(selecionado) {
  const responsaveis = await apiGet("/responsaveis/?ativo=true");
  selectResponsavel.innerHTML = '<option value="">Selecione um responsável</option>' +
    responsaveis.map((item) => `<option value="${item.id}" ${String(item.id) === String(selecionado) ? "selected" : ""}>${item.nome}</option>`).join("");
}

async function inicializar() {
  try {
    await carregarResponsaveis();
    if (obraId) {
      document.getElementById("titulo-formulario").textContent = "Editar Obra";
      const obra = await apiGet(`/obra/${obraId}`);
      for (const [campo, valor] of Object.entries({
        projeto: obra.projeto, data_inicio: obra.data_inicio, data_conclusao: obra.data_conclusao,
        status: obra.status, orcamento: obra.orcamento, endereco: obra.endereco, descricao: obra.descricao,
        contratante: obra.contratante, telefone: obra.telefone, email_contratante: obra.email_contratante,
      })) formObra.elements[campo].value = valor ?? "";
      selectResponsavel.value = obra.id_responsavel;
    }
  } catch (erro) { mostrarMensagem(erro.message, true); }
}

formObra.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const dados = Object.fromEntries(new FormData(formObra));
  if (dados.data_conclusao < dados.data_inicio) return mostrarMensagem("A conclusão não pode ser anterior ao início.", true);
  dados.id_responsavel = Number(dados.id_responsavel);
  if (!dados.orcamento) delete dados.orcamento;
  try {
    if (obraId) await apiPut(`/obra/${obraId}`, dados);
    else await apiPost("/obras", dados);
    window.location.href = "index.html";
  } catch (erro) { mostrarMensagem(erro.message, true); }
});

document.getElementById("novo-responsavel").addEventListener("click", () => modalResponsavel.showModal());
document.getElementById("form-responsavel").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const form = evento.currentTarget;
  try {
    const responsavel = await apiPost("/responsaveis/", Object.fromEntries(new FormData(form)));
    await carregarResponsaveis(responsavel.id);
    modalResponsavel.close();
    form.reset();
  } catch (erro) { window.alert(erro.message); }
});

inicializar();
