import { useMemo, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import TicketModal from "../components/TicketModal";
import { ui } from "../ui/ui";
import StatusBadge from "../components/StatusBadge";

const STATUS_OPTIONS = [
  { value: "", label: "Todos" },
  { value: "open", label: "Aberto" },
  { value: "in_progress", label: "Em andamento" },
  { value: "resolved", label: "Resolvido" },
  { value: "canceled", label: "Cancelado" },
];

export default function SearchPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const t = ui.tokens;

  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [mode, setMode] = useState("text");
  const [q, setQ] = useState("");
  const [ticketId, setTicketId] = useState("");
  const [status, setStatus] = useState("");

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  const canSearch = useMemo(() => {
    if (!user) return false;
    if (user.role === "client") return true;
    return (
      user.role === "support" &&
      (user.position_team === "senior" || user.position_team === "engineer")
    );
  }, [user]);

  async function handleSearch(e) {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);
    setResults([]);

    try {
      const params = new URLSearchParams();
      params.set("mode", mode);
      if (status) params.set("status", status);

      if (mode === "id") {
        const cleaned = ticketId.trim();
        if (!cleaned) throw new Error("Informe o ID do chamado.");
        const n = Number(cleaned);
        if (!Number.isInteger(n) || n <= 0) throw new Error("ID do chamado inválido.");
        params.set("ticket_id", String(n));
      } else {
        const cleaned = q.trim();
        if (!cleaned) throw new Error("Informe o texto da busca.");
        params.set("q", cleaned);
      }

      const res = await api.get(`/tickets/search?${params.toString()}`);
      setResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      setErrorMsg(err?.response?.data?.detail || err?.message || "Erro ao buscar.");
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
    navigate("/");
  }

  function openTicket(id) {
    setSelectedTicketId(id);
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
    setSelectedTicketId(null);
  }

  function handleStatusUpdated(updatedTicket) {
    if (!updatedTicket?.ticket_id) return;

    setResults((prev) =>
      prev.map((r) =>
        r.ticket_id === updatedTicket.ticket_id
          ? {
              ...r,
              status: updatedTicket.status,
              resolution_date: updatedTicket.resolution_date,
            }
          : r
      )
    );
  }

  return (
    <div style={ui.page}>
      {/* HEADER */}
      <div style={ui.headerRow(t)}>
        <div>
          <h1 style={ui.title(t)}>Buscar Chamados</h1>
          <p style={ui.subtitle(t)}>
            Encontre chamados por texto ou por ID e abra o modal para detalhes e ações.
          </p>
        </div>

        <div style={ui.toolbar}>
          <button type="button" style={ui.button("secondary")} onClick={() => navigate("/home")}>
            Início
          </button>
          <button
            type="button"
            style={ui.button("secondary")}
            onClick={() => navigate("/tickets/kanban")}
          >
            Kanban
          </button>
          <button type="button" style={ui.button("danger")} onClick={handleLogout}>
            Sair
          </button>
        </div>
      </div>

      {/* PERMISSÃO */}
      {!canSearch ? (
        <div style={ui.alert("error")}>
            Sem permissão para buscar (apenas clientes ou suportes senior/engineer).
        </div>
      ) : (
        <>
          {/* FILTROS */}
          <div style={ui.card(t)}>
            <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 12 }}>
              <h3 style={ui.sectionTitle(t)}>Filtros</h3>
              <div style={{ fontSize: t.font.size.xs, color: t.colors.subtle }}>
                Dica: use <b>modo ID</b> para busca exata.
              </div>
            </div>

            <form onSubmit={handleSearch} style={{ display: "grid", gap: 12 }}>
              <div style={ui.row}>
                <label style={ui.label(t)}>
                  Modo
                  <select style={ui.select(t)} value={mode} onChange={(e) => setMode(e.target.value)}>
                    <option value="text">Texto</option>
                    <option value="id">ID</option>
                  </select>
                </label>

                {mode === "id" ? (
                  <label style={ui.label(t)}>
                    ID do chamado
                    <input
                      style={ui.input(t)}
                      value={ticketId}
                      onChange={(e) => setTicketId(e.target.value)}
                      placeholder="Ex: 12"
                    />
                  </label>
                ) : (
                  <label style={{ ...ui.label(t), minWidth: 320 }}>
                    Texto
                    <input
                      style={ui.input(t)}
                      value={q}
                      onChange={(e) => setQ(e.target.value)}
                      placeholder="Ex: senha, acesso, erro no sistema..."
                    />
                  </label>
                )}

                <label style={ui.label(t)}>
                  Status
                  <select style={ui.select(t)} value={status} onChange={(e) => setStatus(e.target.value)}>
                    {STATUS_OPTIONS.map((s) => (
                      <option key={s.value} value={s.value}>
                        {s.label}
                      </option>
                    ))}
                  </select>
                </label>

                <button style={ui.button("primary")} disabled={loading} type="submit">
                  {loading ? "Buscando..." : "Buscar"}
                </button>
              </div>

              {errorMsg ? <div style={ui.alert("error")}>{errorMsg}</div> : null}
            </form>
          </div>

          {/* RESULTADOS */}
          <div style={ui.card(t)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
              <h3 style={ui.sectionTitle(t)}>Resultados</h3>
              <span style={{ color: t.colors.muted, fontSize: t.font.size.sm }}>
                {results.length} resultado(s)
              </span>
            </div>

            {loading ? (
              <div style={ui.emptyState()}>
                <div style={ui.spinner()} />
                <div>Buscando resultados...</div>
              </div>
            ) : results.length === 0 ? (
              <div style={ui.emptyState()}>
                <div>Nenhum resultado. Ajuste os filtros e tente novamente.</div>
              </div>
            ) : (
              <div style={ui.tableWrap()}>
                <table style={ui.table}>
                  <thead>
                    <tr>
                      {[
                        "ID",
                        "Status",
                        "Criado em",
                        "Cliente",
                        "Categoria",
                        "Nível",
                        "Suporte",
                        "Assunto",
                      ].map((h) => (
                        <th key={h} style={ui.th()}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((r) => (
                      <tr
                        key={r.ticket_id}
                        onClick={() => openTicket(r.ticket_id)}
                        title="Clique para ver detalhes"
                        style={rowStyle}
                      >
                        <td style={ui.td()}>{r.ticket_id}</td>
                        <td style={ui.td()}><StatusBadge status={r.status} /></td>
                        <td style={ui.td()}>{r.create_date}</td>
                        <td style={ui.td()}>{r.client_name}</td>
                        <td style={ui.td()}>{r.category_name}</td>
                        <td style={ui.td()}>{r.required_level}</td>
                        <td style={ui.td()}>{r.support_name ?? "-"}</td>
                        <td style={ui.td()}>{r.subject_user ?? "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <div style={{ padding: "10px 12px", fontSize: t.font.size.xs, color: t.colors.subtle }}>
                  Clique em uma linha para abrir o chamado no modal.
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {/* MODAL */}
      <TicketModal
        isOpen={isModalOpen}
        onClose={closeModal}
        ticketId={selectedTicketId}
        user={user}
        onStatusUpdated={handleStatusUpdated}
      />
    </div>
  );
}

const rowStyle = {
  cursor: "pointer",
  transition: "background 120ms ease",
};
