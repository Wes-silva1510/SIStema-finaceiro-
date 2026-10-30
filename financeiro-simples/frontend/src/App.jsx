import { useEffect, useState } from "react";
import * as api from "./api.js";

const brl = (v) =>
  Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export default function App() {
  const [accounts, setAccounts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [message, setMessage] = useState(null); // { type, text }

  const [name, setName] = useState("");
  const [initial, setInitial] = useState("");

  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [amount, setAmount] = useState("");
  const [sending, setSending] = useState(false);

  async function loadAccounts() {
    try {
      setAccounts(await api.getAccounts());
    } catch {
      setMessage({ type: "error", text: "Não foi possível falar com a API. O Django está rodando?" });
    }
  }

  async function loadTransactions(id) {
    setSelected(id);
    setTransactions(await api.getTransactions(id));
  }

  useEffect(() => {
    loadAccounts();
  }, []);

  async function handleCreate(e) {
    e.preventDefault();
    try {
      await api.createAccount({ owner_name: name, balance: initial || "0.00" });
      setName("");
      setInitial("");
      setMessage({ type: "ok", text: "Conta criada." });
      loadAccounts();
    } catch (err) {
      setMessage({ type: "error", text: err.message });
    }
  }

  async function handleTransfer(e) {
    e.preventDefault();
    setSending(true); // evita clique duplo
    try {
      await api.transfer({
        from_account: Number(from),
        to_account: Number(to),
        amount,
        idempotency_key: crypto.randomUUID(),
      });
      setAmount("");
      setMessage({ type: "ok", text: "Transferência realizada." });
      await loadAccounts();
      if (selected) loadTransactions(selected);
    } catch (err) {
      setMessage({ type: "error", text: err.message });
    } finally {
      setSending(false);
    }
  }

  return (
    <main>
      <h1>Mini Sistema Financeiro</h1>
      {message && <p className={`msg ${message.type}`}>{message.text}</p>}

      <section>
        <h2>Nova conta</h2>
        <form onSubmit={handleCreate}>
          <input placeholder="Nome do titular" value={name} onChange={(e) => setName(e.target.value)} required />
          <input placeholder="Saldo inicial" type="number" step="0.01" min="0" value={initial} onChange={(e) => setInitial(e.target.value)} />
          <button>Criar</button>
        </form>
      </section>

      <section>
        <h2>Contas</h2>
        <ul>
          {accounts.map((a) => (
            <li key={a.id}>
              <span>#{a.id} {a.owner_name}</span>
              <strong>{brl(a.balance)}</strong>
              <button onClick={() => loadTransactions(a.id)}>Extrato</button>
            </li>
          ))}
          {accounts.length === 0 && <li>Nenhuma conta ainda.</li>}
        </ul>
      </section>

      <section>
        <h2>Transferir</h2>
        <form onSubmit={handleTransfer}>
          <select value={from} onChange={(e) => setFrom(e.target.value)} required>
            <option value="">De...</option>
            {accounts.map((a) => <option key={a.id} value={a.id}>{a.owner_name}</option>)}
          </select>
          <select value={to} onChange={(e) => setTo(e.target.value)} required>
            <option value="">Para...</option>
            {accounts.map((a) => <option key={a.id} value={a.id}>{a.owner_name}</option>)}
          </select>
          <input placeholder="Valor" type="number" step="0.01" min="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} required />
          <button disabled={sending}>{sending ? "Enviando..." : "Transferir"}</button>
        </form>
      </section>

      {selected && (
        <section>
          <h2>Extrato da conta #{selected}</h2>
          <ul>
            {transactions.map((t) => (
              <li key={t.id}>
                <span>{t.description}</span>
                <strong className={Number(t.amount) < 0 ? "neg" : "pos"}>{brl(t.amount)}</strong>
              </li>
            ))}
            {transactions.length === 0 && <li>Sem lançamentos.</li>}
          </ul>
        </section>
      )}
    </main>
  );
}
