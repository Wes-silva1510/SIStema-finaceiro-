const API = "http://localhost:8000/api";

async function request(path, options) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg =
      data.detail ||
      Object.values(data).flat().join(" ") ||
      "Erro inesperado.";
    throw new Error(msg);
  }
  return data;
}

export const getAccounts = () => request("/accounts/");
export const getTransactions = (id) => request(`/accounts/${id}/transactions/`);
export const createAccount = (body) =>
  request("/accounts/", { method: "POST", body: JSON.stringify(body) });
export const transfer = (body) =>
  request("/transfers/", { method: "POST", body: JSON.stringify(body) });
