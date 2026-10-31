/**
 * Configuração central de acesso à API.
 * Este é o ÚNICO lugar que precisa mudar quando o back-end for publicado
 * em um endereço diferente do localhost.
 */
const BASE_URL = "https://projeto-pi2-univesp-grupo13.onrender.com"; // troque pela URL do back publicado

async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(await mensagemErro(res, `Erro ao buscar ${path}`));
  return res.json();
}

async function apiPost(path, dados) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  if (!res.ok) throw new Error(await mensagemErro(res, `Erro ao enviar para ${path}`));
  return res.json();
}

async function apiPut(path, dados) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
  if (!res.ok) throw new Error(await mensagemErro(res, `Erro ao atualizar ${path}`));
  return res.json();
}

async function apiDelete(path) {
  const res = await fetch(`${BASE_URL}${path}`, { method: "DELETE" });
  if (!res.ok) throw new Error(await mensagemErro(res, `Erro ao excluir ${path}`));
  return res.json();
}

async function mensagemErro(res, prefixo) {
  try {
    const body = await res.json();
    return `${prefixo}: ${body.detail || res.status}`;
  } catch {
    return `${prefixo}: ${res.status}`;
  }
}

async function apiDownload(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(await mensagemErro(res, `Erro ao exportar ${path}`));
  return res.blob();
}
