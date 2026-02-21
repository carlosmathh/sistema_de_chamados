import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import StatusBadge from "../components/StatusBadge";
import { ui } from "../ui/ui";

const STATUS_OPTIONS = [
  { value: "open", label: "Aberto" },
  { value: "in_progress", label: "Em andamento" },
  { value: "resolved", label: "Resolvido" },
  { value: "canceled", label: "Cancelado" },
];

const EVENT_LABEL = {
  created: "Criado",
  assigned: "Atribuído",
  reassigned: "Reatribuído",
  status_changed: "Status alterado",
};

export default function TicketModal({
  isOpen,
  onClose,
  ticketId,
  user,
  onStatusUpdated,
}) {
  const t = ui.tokens;

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const [details, setDetails] = useState(null);
  const [newStatus, setNewStatus] = useState("");

  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");

  const [supports, setSupports] = useState([]);
  const [supportsLoading, setSupportsLoading] = useState(false);
  const [supportsError, setSupportsError] = useState("");
  const [newSupportId, setNewSupportId] = useState("");
  const [reassigning, setReassigning] = useState(false);

  const canChangeStatus = user?.role === "support";

  const isSeniorEngineer = useMemo(() => {
    return (
      user?.role === "support" &&
      ["senior", "engineer"].includes(user?.position_team)
    );
  }, [user?.role, user?.position_team]);

  // =========================
  // Load ticket details
  // =========================
  useEffect(() => {
    if (!isOpen || !ticketId) {
      setDetails(null);
      setErrorMsg("");
      setNewStatus("");
      setSupports([]);
      setSupportsError("");
      setNewSupportId("");
      return;
    }

    let cancelled = false;

    async function load() {
      setLoading(true);
      setErrorMsg("");
      setDetails(null);
      setNewStatus("");

      setSupports([]);
      setSupportsError("");
      setNewSupportId("");

      try {
        const res = await api.get(`/tickets/${ticketId}`);
        if (cancelled) return;

        setDetails(res.data);
        setNewStatus(res.data?.status || "");

        // Só busca supports se for senior/engineer e o ticket estiver in_progress
        if (isSeniorEngineer && res.data?.status === "in_progress") {
          setSupportsLoading(true);
          setSupportsError("");

          try {
            const supRes = await api.get(`/tickets/${ticketId}/available-supports`);
            if (cancelled) return;

            setSupports(Array.isArray(supRes.data) ? supRes.data : []);
          } catch (e) {
            if (!cancelled) setSupportsError("Erro ao carregar suportes disponíveis.");
          } finally {
            if (!cancelled) setSupportsLoading(false);
          }
        }
      } catch (err) {
        const detail = err?.response?.data?.detail;
        const code = err?.response?.status;

        if (!cancelled) {
          setErrorMsg(
            typeof detail === "string"
              ? `${detail} (${code})`
              : `Erro ao carregar ticket. (${code || "?"})`
          );
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [isOpen, ticketId, isSeniorEngineer]);

  // =========================
  // Load ticket history
  // =========================
  useEffect(() => {
    if (!isOpen || !ticketId) {
      setHistory([]);
      setHistoryError("");
      return;
    }

    let cancelled = false;

    async function loadHistory() {
      setHistoryLoading(true);
      setHistoryError("");
      setHistory([]);

      try {
        const res = await api.get(`/tickets/${ticketId}/history`);
        if (cancelled) return;

        setHistory(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        if (!cancelled) setHistoryError("Erro ao carregar histórico.");
      } finally {
        if (!cancelled) setHistoryLoading(false);
      }
    }

    loadHistory();
    return () => {
      cancelled = true;
    };
  }, [isOpen, ticketId]);

  async function handleReassign() {
    if (!ticketId || !newSupportId) return;

    setReassigning(true);
    setErrorMsg("");

    try {
      const res = await api.patch(`/tickets/${ticketId}/assign`, {
        support_id: Number(newSupportId),
      });
      const updated = res.data;

      setDetails(updated);
      onStatusUpdated?.(updated);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      const code = err?.response?.status;
      setErrorMsg(
        typeof detail === "string"
          ? `${detail} (${code})`
          : "Erro ao reatribuir ticket."
      );
    } finally {
      setReassigning(false);
    }
  }

  async function handleSaveStatus() {
    if (!ticketId || !newStatus) return;

    setSaving(true);
    setErrorMsg("");

    try {
      const res = await api.patch(`/tickets/${ticketId}/status`, {
        status: newStatus,
      });

      const updated = res.data;

      setDetails(updated);
      setNewStatus(updated?.status || newStatus);
      onStatusUpdated?.(updated);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      const code = err?.response?.status;
      setErrorMsg(
        typeof detail === "string"
          ? `${detail} (${code})`
          : `Erro ao salvar status. (${code || "?"})`
      );
    } finally {
      setSaving(false);
    }
  }

  if (!isOpen) return null;

  const statusChanged = details && newStatus && newStatus !== details.status;

  return (
    <div onClick={onClose} style={ui.overlay()}>
      <div onClick={(e) => e.stopPropagation()} style={ui.modal()}>
        {/* HEADER */}
        <div style={ui.modalHeader()}>
          <div style={{ display: "grid", gap: 4 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap" }}>
              <strong style={{ fontSize: t.font.size.lg, color: t.colors.text }}>
                Chamado #{ticketId}
              </strong>
              {details?.status ? <StatusBadge status={details.status} /> : null}
            </div>

            {details?.client_name ? (
              <span style={{ fontSize: t.font.size.sm, color: t.colors.subtle }}>
                Cliente: <b style={{ color: t.colors.text }}>{details.client_name}</b>
              </span>
            ) : null}
          </div>

          <button style={ui.button("secondary")} onClick={onClose}>
            Fechar
          </button>
        </div>

        {/* BODY */}
        <div style={ui.modalBody()}>
          {loading ? (
            <div style={ui.emptyState()}>
              <div style={ui.spinner()} />
              <div>Carregando ticket...</div>
            </div>
          ) : errorMsg ? (
            <div style={ui.alert("error")}>{errorMsg}</div>
          ) : !details ? (
            <div style={ui.emptyState()}>
              <div>Nenhum dado.</div>
            </div>
          ) : (
            <>
              {/* RESUMO */}
              <div style={ui.section()}>
                <div style={ui.sectionHeader()}>
                  <h3 style={ui.sectionTitle(t)}>Resumo</h3>
                </div>

                <div style={ui.infoGrid}>
                  <Info label="Status" value={<StatusBadge status={details.status} />} />
                  <Info label="Categoria" value={details.category_name} />
                  <Info label="Nível requerido" value={details.required_level} />
                  <Info label="Suporte" value={details.support_name ?? "-"} />
                  <Info label="Criado em" value={details.create_date} />
                  <Info label="Resolvido em" value={details.resolution_date ?? "-"} />
                </div>
              </div>

              {/* ASSUNTO / DESCRIÇÃO */}
              <div style={ui.section()}>
                <div style={ui.sectionHeader()}>
                  <h3 style={ui.sectionTitle(t)}>Detalhes</h3>
                </div>

                <div style={{ display: "grid", gap: 12 }}>
                  <div>
                    <div style={ui.fieldTitle()}>Assunto</div>
                    <Box value={details.subject_user ?? "-"} />
                  </div>

                  <div>
                    <div style={ui.fieldTitle()}>Descrição</div>
                    <Box value={details.description_user ?? "-"} />
                  </div>
                </div>
              </div>

              {/* HISTÓRICO */}
              <div style={ui.section()}>
                <div style={ui.sectionHeader()}>
                  <h3 style={ui.sectionTitle(t)}>Histórico</h3>
                </div>

                {historyLoading ? (
                  <div style={ui.emptyState({ padding: 14 })}>
                    <div style={ui.spinner()} />
                    <div>Carregando histórico...</div>
                  </div>
                ) : historyError ? (
                  <div style={ui.alert("error")}>{historyError}</div>
                ) : history.length === 0 ? (
                  <div style={ui.emptyState({ padding: 14 })}>Sem histórico.</div>
                ) : (
                  <div style={ui.tableWrap()}>
                    <table style={ui.table}>
                      <thead>
                        <tr>
                          {["Data", "Evento", "De", "Para", "Ator", "Obs."].map((h) => (
                            <th key={h} style={ui.th()}>{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {history.map((row) => (
                          <tr key={row.id ?? `${row.created_at}-${row.event_type}`}>
                            <td style={ui.td()}>{formatDate(row.created_at)}</td>
                            <td style={ui.td()}>{EVENT_LABEL[row.event_type] ?? row.event_type ?? "-"}</td>
                            <td style={ui.td()}>
                              {row.old_value ? <StatusBadge status={row.old_value} /> : "-"}
                            </td>
                            <td style={ui.td()}>
                              {row.new_value ? <StatusBadge status={row.new_value} /> : "-"}
                            </td>
                            <td style={ui.td()}>
                              {row.actor_type ?? "-"} {row.actor_id ? `#${row.actor_id}` : ""}
                            </td>
                            <td style={ui.td()}>{row.note ?? "-"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>

              {/* AÇÕES */}
              {(canChangeStatus || (isSeniorEngineer && details?.status === "in_progress")) && (
                <div style={ui.section()}>
                  <div style={ui.sectionHeader()}>
                    <h3 style={ui.sectionTitle(t)}>Ações</h3>
                  </div>

                  {/* ALTERAR STATUS */}
                  {canChangeStatus && (
                    <div style={ui.actionRow()}>
                      <div style={ui.actionGroup()}>
                        <label style={ui.label(t)}>
                          Alterar status
                          <select
                            value={newStatus}
                            onChange={(e) => setNewStatus(e.target.value)}
                            style={ui.select(t)}
                          >
                            {STATUS_OPTIONS.map((s) => (
                              <option key={s.value} value={s.value}>
                                {s.label}
                              </option>
                            ))}
                          </select>
                        </label>
                        <div style={ui.hint()}>
                          {statusChanged ? "Pronto para salvar a mudança." : "Selecione um status diferente para salvar."}
                        </div>
                      </div>

                      <button
                        style={ui.button("primary")}
                        onClick={handleSaveStatus}
                        disabled={saving || !details || !statusChanged}
                      >
                        {saving ? "Salvando..." : "Salvar"}
                      </button>
                    </div>
                  )}

                  {/* REATRIBUIR */}
                  {isSeniorEngineer && details?.status === "in_progress" && (
                    <div style={ui.actionRow({ marginTop: 12 })}>
                      <div style={ui.actionGroup()}>
                        <label style={ui.label(t)}>
                          Reatribuir para
                          <select
                            value={newSupportId}
                            onChange={(e) => setNewSupportId(e.target.value)}
                            style={ui.select(t)}
                            disabled={supportsLoading}
                          >
                            <option value="">Selecione</option>
                            {supports.map((s) => (
                              <option key={s.id} value={s.id}>
                                {s.name} ({s.position_team}) • em andamento: {s.in_progress_count}
                              </option>
                            ))}
                          </select>
                        </label>

                        {supportsLoading ? (
                          <div style={ui.hint()}>Carregando suportes...</div>
                        ) : supportsError ? (
                          <div style={ui.errorText()}>{supportsError}</div>
                        ) : (
                          <div style={ui.hint()}>
                            Só aparecem suportes elegíveis (nível e limite em andamento).
                          </div>
                        )}
                      </div>

                      <button
                        style={ui.button("primary")}
                        onClick={handleReassign}
                        disabled={reassigning || !newSupportId}
                      >
                        {reassigning ? "Reatribuindo..." : "Reatribuir"}
                      </button>
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function Info({ label, value }) {
  const t = ui.tokens;
  return (
    <div style={ui.infoBox()}>
      <div style={ui.infoLabel()}>{label}</div>
      <div style={ui.infoValue()}>{value === null || value === undefined ? "-" : value}</div>
    </div>
  );
}

function Box({ value }) {
  const t = ui.tokens;
  return (
    <div style={ui.box()}>
      {String(value)}
    </div>
  );
}

function formatDate(v) {
  if (!v) return "-";
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? String(v) : d.toLocaleString();
}
