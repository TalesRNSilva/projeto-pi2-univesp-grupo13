/**
 * Configuração central de acesso à API.
 * Este é o ÚNICO lugar que precisa mudar quando o back-end for publicado
 * em um endereço diferente do localhost.
 */
const BASE_URL = "http://localhost:8000"; // troque pela URL do back publicado

async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`Erro ao buscar ${path}: ${res.status}`);
  return res.json();
}

async function apiPost(path, dados) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  if (!res.ok) throw new Error(`Erro ao enviar para ${path}: ${res.status}`);
  return res.json();
}

async function apiPut(path, dados) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  if (!res.ok) throw new Error(`Erro ao atualizar ${path}: ${res.status}`);
  return res.json();
}

async function apiDelete(path) {
  const res = await fetch(`${BASE_URL}${path}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Erro ao excluir ${path}: ${res.status}`);
  return res.json();
}
