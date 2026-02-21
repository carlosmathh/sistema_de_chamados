import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import TicketModal from "../components/TicketModal";
import StatusBadge from "../components/StatusBadge";
import { ui } from "../ui/ui";

const COLUMNS = [
  { key: "open", title: "Aberto" },
  { key: "in_progress", title: "Em andamento" },
  { key: "resolved", title: "Resolvido" },
  { key: "canceled", title: "Cancelado" },
];

const STATUS_LABEL = {
  open: "Aberto",
  in_progress: "Em andamento",
  resolved: "Resolvido",
  canceled: "Cancelado",
};

export default function TicketsKanbanPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const t = ui.tokens;

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const [tickets, setTickets] = useState([]);

  const [selectedTicketId, setSelectedTicketId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [draggingId, setDraggingId] = useState(null);
  const [savingMap, setSavingMap] = useState({}); // { [ticket_id]: true }

  const isSeniorEngineer =
    user?.role === "support" && ["senior", "engineer"].includes(user?.position_team);

  useEffect(() => {
    loadAll();
  }, []);

  async function loadAll() {
    setLoading(true);
    setErrorMsg("");
    try {
      const res = await api.get("/tickets/board?status=all");
      setTickets(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      setErrorMsg(err?.response?.data?.detail || "Erro ao carregar kanban.");
      setTickets([]);
    } finally {
      setLoading(false);
    }
  }

  const grouped = useMemo(() => {
    const map = { open: [], in_progress: [], resolved: [], canceled: [] };

    for (const tk of tickets) {
      const st = tk?.status;
      if (map[st]) map[st].push(tk);
    }

    for (const k of Object.keys(map)) {
      map[k].sort((a, b) => String(a.create_date).localeCompare(String(b.create_date)));
    }

    return map;
  }, [tickets]);

  function openTicket(id) {
    setSelectedTicketId(id);
    setIsModalOpen(true);
  }

  function closeModal() {
    setIsModalOpen(false);
    setSelectedTicketId(null);
  }

  function handleTicketUpdated(updated) {
    if (!updated?.ticket_id) return;
    setTickets((prev) => prev.map((t) => (t.ticket_id === updated.ticket_id ? { ...t, ...updated } : t)));
  }

  function onDragStart(ticketId) {
    setDraggingId(ticketId);
  }

  function onDragEnd() {
    setDraggingId(null);
  }

  function allowDrop(e) {
    e.preventDefault();
  }

  async function moveTicket(ticketId, toStatus) {
    const current = tickets.find((t) => t.ticket_id === ticketId);
    if (!current) return;

    const fromStatus = current.status;
    if (fromStatus === toStatus) return;

    // optimistic update
    setTickets((prev) =>
      prev.map((t) => (t.ticket_id === ticketId ? { ...t, status: toStatus } : t))
    );

    setSavingMap((m) => ({ ...m, [ticketId]: true }));
    setErrorMsg("");

    try {
      const res = await api.patch(`/tickets/${ticketId}/status`, { status: toStatus });
      const updated = res.data;

      setTickets((prev) =>
        prev.map((t) => (t.ticket_id === ticketId ? { ...t, ...updated } : t))
      );
    } catch (err) {
      // rollback
      setTickets((prev) =>
        prev.map((t) => (t.ticket_id === ticketId ? { ...t, status: fromStatus } : t))
      );

      const detail = err?.response?.data?.detail;
      setErrorMsg(detail ||`Não foi possível mover o chamado #${ticketId} para "${STATUS_LABEL[toStatus] ?? toStatus}".`);
    } finally {
      setSavingMap((m) => {
        const copy = { ...m };
        delete copy[ticketId];
        return copy;
      });
    }
  }

  if (user && !isSeniorEngineer) {
    return (
      <div style={ui.page}>
        <div style={ui.headerRow(t)}>
          <div>
            <h1 style={ui.title(t)}>Kanban</h1>
            <p style={ui.subtitle(t)}>Acesso restrito.</p>
          </div>
          <div style={ui.toolbar}>
            <button style={ui.button("secondary")} onClick={() => navigate("/home")}>
              Início
            </button>
          </div>
        </div>

        <div style={ui.alert("error")}>
          Acesso permitido apenas para suportes senior e engineer.
        </div>
      </div>
    );
  }

  return (
    <div style={{ ...ui.page, maxWidth: 1400 }}>
      {/* HEADER */}
      <div style={ui.headerRow(t)}>
        <div>
          <h1 style={ui.title(t)}>Kanban</h1>
          <p style={ui.subtitle(t)}>Arraste chamados entre colunas para atualizar o status.</p>
        </div>

        <div style={ui.toolbar}>
          <button style={ui.button("secondary")} onClick={() => navigate("/home")}>
            Início
          </button>
          <button style={ui.button("secondary")} onClick={() => navigate("/search")}>
            Buscar
          </button>
          <button style={ui.button("primary")} disabled={loading} onClick={loadAll}>
            {loading ? "Atualizando..." : "Atualizar"}
          </button>
        </div>
      </div>

      {errorMsg ? <div style={ui.alert("error")}>{errorMsg}</div> : null}

      {loading && tickets.length === 0 ? (
        <div style={{ marginTop: 16 }}>
          <div style={ui.emptyState()}>
            <div style={ui.spinner()} />
            <div>Carregando Kanban...</div>
          </div>
        </div>
      ) : (
        <div
          style={{
            marginTop: 16,
            display: "grid",
            gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
            gap: 12,
            alignItems: "start",
          }}
        >
          {COLUMNS.map((col) => (
            <Column
              key={col.key}
              title={col.title}
              statusKey={col.key}
              tickets={grouped[col.key]}
              allowDrop={allowDrop}
              onDropTicket={(ticketId) => moveTicket(ticketId, col.key)}
              onOpenTicket={openTicket}
              draggingId={draggingId}
              savingMap={savingMap}
              onDragStart={onDragStart}
              onDragEnd={onDragEnd}
            />
          ))}
        </div>
      )}

      {/* MODAL */}
      <TicketModal
        isOpen={isModalOpen}
        onClose={closeModal}
        ticketId={selectedTicketId}
        user={user}
        onStatusUpdated={handleTicketUpdated}
      />
    </div>
  );
}

function Column({
  title,
  statusKey,
  tickets,
  allowDrop,
  onDropTicket,
  onOpenTicket,
  draggingId,
  savingMap,
  onDragStart,
  onDragEnd,
}) {
  const t = ui.tokens;
  const [isOver, setIsOver] = useState(false);

  const count = tickets.length;

  return (
    <div
      onDragOver={(e) => {
        allowDrop(e);
        setIsOver(true);
      }}
      onDragLeave={() => setIsOver(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsOver(false);
        const id = Number(e.dataTransfer.getData("text/plain"));
        if (!Number.isNaN(id)) onDropTicket(id);
      }}
      style={{
        border: `1px solid ${t.colors.border}`,
        borderRadius: t.radius.lg,
        background: isOver ? t.colors.surface2 : t.colors.surface,
        padding: 12,
        minHeight: 520,
        boxShadow: isOver ? t.shadow.md : t.shadow.sm,
        transition: `background ${t.motion.fast}, box-shadow ${t.motion.fast}`,
      }}
    >
      {/* HEADER COLUNA */}
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 10 }}>
        <div style={{ fontWeight: t.font.weight.extrabold, color: t.colors.text }}>
          {title}
        </div>
        <div
          style={{
            fontSize: t.font.size.xs,
            color: t.colors.muted,
            border: `1px solid ${t.colors.border}`,
            borderRadius: 999,
            padding: "2px 8px",
            background: t.colors.surface2,
          }}
        >
          {count}
        </div>
      </div>

      {/* LISTA */}
      <div style={{ marginTop: 10, display: "grid", gap: 10 }}>
        {tickets.map((tk) => {
          const realId = tk.ticket_id ?? tk.id;

          return (
            <TicketCard
              key={realId}
              ticket={tk}
              onOpen={() => onOpenTicket(realId)}
              dragging={draggingId === realId}
              saving={!!savingMap[realId]}
              onDragStart={() => onDragStart(realId)}
              onDragEnd={onDragEnd}
            />
          );
        })}

        {tickets.length === 0 && (
          <div style={{ color: t.colors.subtle, fontSize: t.font.size.sm, padding: 10 }}>
            Vazio.
          </div>
        )}
      </div>

      {/* DROP HINT */}
      {isOver && (
        <div style={{ marginTop: 10, ...ui.hint() }}>
          Solte aqui para mover para <b>{title}</b>.
        </div>
      )}
    </div>
  );
}

function TicketCard({ ticket, onOpen, dragging, saving, onDragStart, onDragEnd }) {
  const t = ui.tokens;

  const realId = ticket.ticket_id ?? ticket.id;

  return (
    <div
      draggable
      onDragStart={(e) => {
        e.dataTransfer.setData("text/plain", String(realId));
        e.dataTransfer.effectAllowed = "move";
        onDragStart?.();
      }}
      onDragEnd={onDragEnd}
      onDoubleClick={onOpen}
      onClick={onOpen}
      title="Arraste para outra coluna • Clique para abrir"
      style={{
        border: dragging ? `2px dashed ${t.colors.text}` : `1px solid ${t.colors.border}`,
        background: t.colors.surface,
        borderRadius: t.radius.md,
        padding: 12,
        cursor: "grab",
        opacity: saving ? 0.65 : 1,
        boxShadow: t.shadow.sm,
        transition: `transform ${t.motion.fast}, box-shadow ${t.motion.fast}, opacity ${t.motion.fast}`,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 10 }}>
        <div style={{ fontWeight: t.font.weight.extrabold, color: t.colors.text }}>
          #{realId}
        </div>
        <StatusBadge status={ticket.status} />
      </div>

      <div style={{ marginTop: 8, fontSize: t.font.size.sm, color: t.colors.text }}>
        <div><b>Cliente:</b> {ticket.client_name}</div>
        <div><b>Categoria:</b> {ticket.category_name}</div>
        <div><b>Nível:</b> {ticket.required_level}</div>
        <div><b>Suporte:</b> {ticket.support_name ?? "-"}</div>
      </div>

      <div style={{ marginTop: 8, fontSize: t.font.size.xs, color: t.colors.muted }}>
        <b>Assunto:</b> {ticket.subject_user ?? "-"}
      </div>

      {saving && (
        <div style={{ marginTop: 8, fontSize: t.font.size.xs, color: t.colors.subtle }}>
          Salvando...
        </div>
      )}
    </div>
  );
}
