/**
 * Lógica da tela de Responsáveis (responsaveis.html).
 */
async function carregarResponsaveis() {
  try {
    const dados = await apiGet("/responsaveis/");
    // TODO: renderizar a lista com botões de editar/remover (soft delete)
    document.getElementById("lista-responsaveis").textContent = JSON.stringify(dados);
  } catch (erro) {
    document.getElementById("lista-responsaveis").textContent = "Erro ao carregar responsáveis.";
    console.error(erro);
  }
}

carregarResponsaveis();

// TODO: capturar o envio do formulário de cadastro e chamar apiPost("/responsaveis/", dados)
