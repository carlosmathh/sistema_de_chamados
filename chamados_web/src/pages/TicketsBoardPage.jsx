import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import TicketModal from "../components/TicketModal";
import StatusBadge from "../components/StatusBadge";

const TABS = [
  { value: "open", label: "Aberto" },
  { value: "in_progress", label: "Em andamento" },
  { value: "resolved", label: "Resolvido" },
  { value: "canceled", label: "Cancelado" },
  { value: "all", label: "Todos" },
];

export default function TicketsBoardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [tab, setTab] = useState("in_progress");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");

  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const title = useMemo(() => {
    return "Quadro de Chamados (Senior/Engineer)";
  }, []);

  useEffect(() => {
    loadBoard();
  }, [tab]);

  async function loadBoard() {
    setErrorMsg("");
    setLoading(true);

    try {
      const res = await api.get(`/tickets/board?status=${tab}`);
      setResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setErrorMsg(detail || "Erro ao carregar quadro.");
      setResults([]);
    } finally {
      setLoading(false);
    }
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

    setResults((prev) => {
      const next = prev.map((r) =>
        r.ticket_id === updatedTicket.ticket_id ? { ...r, ...updatedTicket } : r
      );

      if (tab === "all") return next;

      return next.filter((r) => r.status === tab);
    });
  }

  return (
    <div style={{ maxWidth: 1100, margin: "40px auto", fontFamily: "system-ui", padding: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "end", gap: 12 }}>
        <div>
          <h1 style={{ margin: 0 }}>{title}</h1>
          <p style={{ margin: "6px 0 0", color: "#555" }}>
            role: <b>{user?.role}</b> • Nível: <b>{user?.position_team}</b>
          </p>
        </div>

        <div style={{ display: "flex", gap: 10 }}>
          <button onClick={() => navigate("/home")}>Início</button>
          <button onClick={() => navigate("/search")}>Buscar</button>
        </div>
      </div>

      <div style={{ marginTop: 16, border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {TABS.map((t) => (
            <TabButton
              key={t.value}
              active={tab === t.value}
              onClick={() => setTab(t.value)}
            >
              {t.label}
            </TabButton>
          ))}

          <button disabled={loading} onClick={loadBoard} style={{ marginLeft: "auto" }}>
            {loading ? "Atualizando..." : "Atualizar"}
          </button>
        </div>

        {errorMsg ? <p style={{ color: "crimson", marginTop: 10 }}>{errorMsg}</p> : null}
        <p style={{ margin: "10px 0 0", color: "#666" }}>
          {loading ? "Carregando..." : `${results.length} chamado(s)`}
        </p>
      </div>

      <div style={{ marginTop: 16 }}>
        {results.length === 0 ? (
          <p style={{ color: "#777" }}>{loading ? "Carregando..." : "Nenhum chamado."}</p>
        ) : (
          <div style={{ overflowX: "auto", marginTop: 12 }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  {[
                    "ID",
                    "Status",
                    "Criado em",
                    "Resolvido em",
                    "Cliente",
                    "Categoria",
                    "Nível",
                    "Suporte"
                  ].map((h) => (
                    <th
                      key={h}
                      style={{
                        textAlign: "left",
                        borderBottom: "1px solid #ddd",
                        padding: "10px 8px",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {results.map((r) => (
                  <tr
                    key={r.ticket_id}
                    onClick={() => openTicket(r.ticket_id)}
                    style={{ cursor: "pointer" }}
                    title="Clique para ver detalhes"
                  >
                    <td style={td}>{r.ticket_id}</td>
                    <td style={td}><StatusBadge status={r.status} /></td>
                    <td style={td}>{r.create_date}</td>
                    <td style={td}>{r.resolution_date ?? "-"}</td>
                    <td style={td}>{r.client_name}</td>
                    <td style={td}>{r.category_name}</td>
                    <td style={td}>{r.required_level}</td>
                    <td style={td}>{r.support_name ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

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

function TabButton({ active, onClick, children }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "10px 12px",
        borderRadius: 999,
        border: active ? "2px solid #111" : "1px solid #ddd",
        background: "#fff",
        cursor: "pointer",
        fontWeight: 600,
      }}
    >
      {children}
    </button>
  );
}

const td = { padding: "10px 8px", borderBottom: "1px solid #f0f0f0" };
