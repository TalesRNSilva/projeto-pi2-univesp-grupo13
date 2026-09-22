/**
 * Lógica da tela de Visualização Geral (index.html).
 */
async function carregarObras() {
  try {
    const dados = await apiGet("/obras/");
    // TODO: renderizar a lista de obras na tela (cartões de status + tabela paginada)
    document.getElementById("lista-obras").textContent = JSON.stringify(dados);
  } catch (erro) {
    document.getElementById("lista-obras").textContent = "Erro ao carregar obras.";
    console.error(erro);
  }
}

carregarObras();
