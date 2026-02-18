const STATUS_LABEL = {
  open: "Open",
  in_progress: "In progress",
  resolved: "Resolved",
  canceled: "Canceled",
};

export default function StatusBadge({ status }) {
  const s = status || "-";

  const styleByStatus = {
    open: { border: "1px solid #e6b800", background: "#fff7cc", color: "#7a5a00" },
    in_progress: { border: "1px solid #3b82f6", background: "#dbeafe", color: "#1d4ed8" },
    resolved: { border: "1px solid #22c55e", background: "#dcfce7", color: "#166534" },
    canceled: { border: "1px solid #ef4444", background: "#fee2e2", color: "#991b1b" },
    "-": { border: "1px solid #ddd", background: "#f7f7f7", color: "#444" },
  };

  const st = styleByStatus[s] ?? styleByStatus["-"];

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        padding: "6px 10px",
        borderRadius: 999,
        fontSize: 12,
        fontWeight: 600,
        lineHeight: 1,
        ...st,
      }}
      title={s}
    >
      {STATUS_LABEL[s] ?? s}
    </span>
  );
}
