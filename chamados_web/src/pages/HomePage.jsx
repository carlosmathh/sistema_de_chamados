import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import TicketModal from "../components/TicketModal";
import StatusBadge from "../components/StatusBadge";
import { ui } from "../ui/ui";

const STATUS_OPTIONS = [
  { value: "", label: "Todos" },
  { value: "open", label: "Open" },
  { value: "in_progress", label: "In progress" },
  { value: "resolved", label: "Resolved" },
  { value: "canceled", label: "Canceled" },
];

const STATUS_ORDER = ["open", "in_progress", "resolved", "canceled"];

const STATUS_LABEL = {
  open: "Open",
  in_progress: "In progress",
  resolved: "Resolved",
  canceled: "Canceled",
};

export default function HomePage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const t = ui.tokens;

  const isSupport = user?.role === "support";
  const isSeniorEngineer = isSupport && ["senior", "engineer"].includes(user?.position_team);
  const isClient = user?.role === "client";

  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const counts = useMemo(() => {
    const base = { all: results.length, open: 0, in_progress: 0, resolved: 0, canceled: 0 };

    for (const tk of results) {
      const st = tk?.status;
      if (base[st] !== undefined) base[st] += 1;
    }

    return base;
  }, [results]);

  const title = useMemo(() => {
    if (!user) return "Meus tickets";
    if (user.role === "client") return "Meus tickets";
    return "Tickets atribuídos a mim";
  }, [user]);

  useEffect(() => {
    if (!user) return;
    loadMyTickets();
  }, [user, status]);

  async function loadMyTickets() {
    setErrorMsg("");
    setLoading(true);

    try {
      const params = new URLSearchParams();
      if (status) params.set("status", status);

      const qs = params.toString();
      const res = await api.get(`/tickets/mine${qs ? `?${qs}` : ""}`);

      setResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      const detail = err?.response?.data?.detail;

      let msg = "Erro ao carregar tickets.";
      if (typeof detail === "string") msg = detail;
      else if (Array.isArray(detail)) msg = detail.map((e) => e?.msg).filter(Boolean).join(" | ");
      else if (detail) msg = JSON.stringify(detail);

      setErrorMsg(msg);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    logout();
    navigate("/");
  }

  function openTicket(ticketId) {
    setSelectedTicketId(ticketId);
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
    setSelectedTicketId(null);
  }

  function handleStatusUpdated(updatedTicket) {
    if (!updatedTicket?.ticket_id) return;

    setResults((prev) =>
      prev.map((r) => (r.ticket_id === updatedTicket.ticket_id ? { ...r, ...updatedTicket } : r))
    );
  }

  return (
    <div style={{ ...ui.page, maxWidth: 1100 }}>
      {/* HEADER */}
      <div style={ui.headerRow(t)}>
        <div>
          <h1 style={ui.title(t)}>{title}</h1>
          <p style={ui.subtitle(t)}>
            Visualize seus tickets, filtre por status e abra detalhes para acompanhar histórico e ações.
          </p>
        </div>

        <div style={ui.toolbar}>
          {isSeniorEngineer ? (
            <button style={ui.button("secondary")} onClick={() => navigate("/tickets/kanban")}>
              Kanban
            </button>
          ) : null}

          {isClient ? (
            <button style={ui.button("primary")} onClick={() => navigate("/tickets/new")}>
              Novo ticket
            </button>
          ) : null}

          {isClient || isSeniorEngineer ? (
            <button style={ui.button("secondary")} onClick={() => navigate("/search")}>
              Buscar
            </button>
          ) : null}

          <button style={ui.button("danger")} onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>

      {/* DASHBOARD */}
      <div style={ui.card(t)}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 12 }}>
          <h3 style={ui.sectionTitle(t)}>Resumo</h3>
          <div style={{ fontSize: t.font.size.xs, color: t.colors.subtle }}>
            {loading ? "Carregando..." : `${results.length} item(s)`}
          </div>
        </div>

        <div
          style={{
            marginTop: 10,
            display: "grid",
            gridTemplateColumns: "repeat(5, minmax(0, 1fr))",
            gap: 10,
          }}
        >
          <DashCard
            title="Todos"
            value={counts.all}
            active={status === ""}
            onClick={() => setStatus("")}
          />

          {STATUS_ORDER.map((st) => (
            <DashCard
              key={st}
              title={STATUS_LABEL[st]}
              value={counts[st]}
              active={status === st}
              onClick={() => setStatus(st)}
            />
          ))}
        </div>

        <div style={{ marginTop: 14, display: "flex", gap: 12, alignItems: "end", flexWrap: "wrap" }}>
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

          <button style={ui.button("primary")} disabled={loading} onClick={loadMyTickets}>
            {loading ? "Atualizando..." : "Atualizar"}
          </button>

          <div style={ui.hint()}>
            Dica: clique em um card acima para filtrar rapidamente.
          </div>
        </div>

        {errorMsg ? <div style={{ marginTop: 12, ...ui.alert("error") }}>{errorMsg}</div> : null}
      </div>

      {/* TABELA */}
      <div style={ui.card(t)}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 12 }}>
          <h3 style={ui.sectionTitle(t)}>Tickets</h3>
          <div style={{ fontSize: t.font.size.xs, color: t.colors.subtle }}>
            Clique em uma linha para abrir o ticket.
          </div>
        </div>

        {loading && results.length === 0 ? (
          <div style={ui.emptyState()}>
            <div style={ui.spinner()} />
            <div>Carregando tickets...</div>
          </div>
        ) : results.length === 0 ? (
          <div style={ui.emptyState()}>
            <div>Nenhum ticket encontrado para este filtro.</div>
          </div>
        ) : (
          <div style={ui.tableWrap()}>
            <table style={ui.table}>
              <thead>
                <tr>
                  {[
                    "ticket_id",
                    "status",
                    "create_date",
                    "resolution_date",
                    "client_name",
                    "category_name",
                    "required_level",
                    "support_name",
                    "subject_user",
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
                    style={{ cursor: "pointer" }}
                    className="table-row"
                  >
                    <td style={ui.td()}>{r.ticket_id}</td>
                    <td style={ui.td()}><StatusBadge status={r.status} /></td>
                    <td style={ui.td()}>{r.create_date}</td>
                    <td style={ui.td()}>{r.resolution_date ?? "-"}</td>
                    <td style={ui.td()}>{r.client_name}</td>
                    <td style={ui.td()}>{r.category_name}</td>
                    <td style={ui.td()}>{r.required_level}</td>
                    <td style={ui.td()}>{r.support_name ?? "-"}</td>
                    <td style={ui.td()}>{r.subject_user ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

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

function DashCard({ title, value, active, onClick }) {
  const t = ui.tokens;

  return (
    <button
      onClick={onClick}
      style={{
        padding: 14,
        borderRadius: t.radius.lg,
        border: active ? `2px solid ${t.colors.text}` : `1px solid ${t.colors.border}`,
        background: t.colors.surface,
        cursor: "pointer",
        textAlign: "left",
        boxShadow: t.shadow.sm,
        transition: `transform ${t.motion.fast}, box-shadow ${t.motion.fast}, border-color ${t.motion.fast}`,
      }}
      className="dash-card"
      type="button"
    >
      <div style={{ fontSize: t.font.size.xs, color: t.colors.subtle, fontWeight: t.font.weight.bold }}>
        {title}
      </div>
      <div style={{ fontSize: t.font.size["2xl"], fontWeight: t.font.weight.extrabold, marginTop: 6 }}>
        {value}
      </div>
    </button>
  );
}
