// src/ui/ui.js



const fontSans =
  'ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji"';

export const ui = {
  // =========================
  // 1) TOKENS (design system)
  // =========================

  

  tokens: {
    font: {
      sans: fontSans,
      size: { xs: 12, sm: 13, md: 14, lg: 16, xl: 20, "2xl": 24 },
      weight: { regular: 400, medium: 500, semibold: 600, bold: 700, extrabold: 800 },
      tracking: { tight: "-0.02em" },
    },

    radius: { sm: 10, md: 12, lg: 14, xl: 16 },

    shadow: {
      sm: "0 6px 18px rgba(2, 6, 23, 0.06)",
      md: "0 12px 30px rgba(2, 6, 23, 0.10)",
      modal: "0 20px 60px rgba(2, 6, 23, 0.35)",
    },

    z: { modal: 9999 },

    motion: {
      fast: "120ms ease",
      base: "180ms ease",
    },

    colors: {
      text: "#0f172a", // slate-900
      muted: "#475569", // slate-600
      subtle: "#64748b", // slate-500

      bg: "#f8fafc", // slate-50 (use no body)
      surface: "#ffffff",
      surface2: "#f8fafc",
      border: "#e2e8f0", // slate-200
      borderStrong: "#cbd5e1", // slate-300

      primary: "#2563eb", // blue-600
      primaryHover: "#1d4ed8", // blue-700
      primarySoft: "rgba(37, 99, 235, 0.20)",

      danger: "#ef4444",
      dangerSoft: "rgba(239, 68, 68, 0.18)",

      infoBg: "#e0f2fe",
      infoBorder: "#bae6fd",
      infoText: "#075985",

      errorBg: "#fee2e2",
      errorBorder: "#fecaca",
      errorText: "#991b1b",

      overlay: "rgba(2,6,23,0.55)", // slate-950
      headerBg: "#fbfdff",
      tableHeadBg: "#f8fafc",
      rowBorder: "#f1f5f9",
    },

    control: {
      h: 38,
      padX: 12,
    },
  },

  // =========================
  // 2) LAYOUT
  // =========================
  page: {
    maxWidth: 1100,
    margin: "28px auto",
    padding: 16,
    fontFamily: fontSans,
    color: "#0f172a",
  },

  headerRow: (t) => ({
    display: "flex",
    justifyContent: "space-between",
    alignItems: "end",
    gap: 12,
    paddingBottom: 12,
    borderBottom: `1px solid ${t.colors.border}`,
  }),

  title: (t) => ({
    margin: 0,
    fontSize: t.font.size["2xl"],
    fontWeight: t.font.weight.extrabold,
    letterSpacing: t.font.tracking.tight,
    color: t.colors.text,
  }),

  subtitle: (t) => ({
    margin: "6px 0 0",
    color: t.colors.muted,
    fontSize: t.font.size.sm,
  }),

  toolbar: {
    display: "flex",
    gap: 8,
    flexWrap: "wrap",
    alignItems: "center",
  },

  row: { display: "flex", gap: 12, flexWrap: "wrap", alignItems: "end" },

  // 3 COMPONENTES BASE

    card: (t) => ({
    marginTop: 16,
    background: "rgba(255,255,255,0.8)",
    backdropFilter: "blur(6px)",
    border: `1px solid ${t.colors.border}`,
    borderRadius: t.radius.lg,
    padding: 14,
    boxShadow: "0 10px 30px rgba(2, 6, 23, 0.08)",
    }),




  sectionTitle: (t) => ({
    margin: "0 0 10px",
    fontSize: t.font.size.md,
    fontWeight: t.font.weight.bold,
    color: t.colors.text,
  }),

  label: (t) => ({
    display: "grid",
    gap: 6,
    fontSize: t.font.size.xs,
    color: "#334155", 
  }),

  input: (t) => ({
    height: t.control.h,
    padding: `0 ${t.control.padX}px`,
    borderRadius: t.radius.sm,
    border: `1px solid ${t.colors.borderStrong}`,
    outline: "none",
    minWidth: 220,
    background: t.colors.surface,
    color: t.colors.text,
    transition: `border-color ${t.motion.fast}, box-shadow ${t.motion.fast}`,
  }),

  select: (t) => ({
    height: t.control.h,
    padding: "0 10px",
    borderRadius: t.radius.sm,
    border: `1px solid ${t.colors.borderStrong}`,
    outline: "none",
    background: t.colors.surface,
    minWidth: 180,
    color: t.colors.text,
    transition: `border-color ${t.motion.fast}, box-shadow ${t.motion.fast}`,
  }),

  textarea: (t) => ({
    padding: 12,
    borderRadius: t.radius.sm,
    border: `1px solid ${t.colors.borderStrong}`,
    outline: "none",
    background: t.colors.surface,
    width: "100%",
    color: t.colors.text,
    transition: `border-color ${t.motion.fast}, box-shadow ${t.motion.fast}`,
  }),

  // Buttons (use variants)
  buttonBase: (t) => ({
    height: t.control.h,
    padding: "0 12px",
    borderRadius: t.radius.sm,
    cursor: "pointer",
    fontWeight: t.font.weight.semibold,
    transition: `transform ${t.motion.fast}, background ${t.motion.fast}, border-color ${t.motion.fast}, box-shadow ${t.motion.fast}, opacity ${t.motion.fast}`,
    userSelect: "none",
  }),

  button: (variant = "default") => {
    const t = ui.tokens;

    const base = ui.buttonBase(t);

    const variants = {
      default: {
        ...base,
        border: `1px solid ${t.colors.borderStrong}`,
        background: t.colors.surface,
        color: t.colors.text,
      },
      primary: {
        ...base,
        padding: "0 14px",
        border: `1px solid ${t.colors.primary}`,
        background: t.colors.primary,
        color: "#fff",
        fontWeight: t.font.weight.bold,
        boxShadow: `0 10px 20px ${t.colors.primarySoft}`,
      },
      danger: {
        ...base,
        padding: "0 14px",
        border: `1px solid ${t.colors.danger}`,
        background: t.colors.danger,
        color: "#fff",
        fontWeight: t.font.weight.bold,
        boxShadow: `0 10px 20px ${t.colors.dangerSoft}`,
      },
      ghost: {
        ...base,
        border: "1px solid transparent",
        background: "transparent",
        color: t.colors.primary,
        fontWeight: t.font.weight.bold,
      },
      secondary: {
        ...base,
        border: `1px solid ${t.colors.border}`,
        background: t.colors.surface2,
        color: t.colors.text,
      },
    };

    return variants[variant] ?? variants.default;
  },

  // Alerts
  alert: (type = "info") => {
    const t = ui.tokens;
    const base = {
      marginTop: 16,
      padding: 12,
      borderRadius: t.radius.md,
      fontWeight: t.font.weight.semibold,
      border: `1px solid ${t.colors.border}`,
      background: t.colors.surface2,
      color: t.colors.text,
    };

    if (type === "error") {
      return {
        ...base,
        border: `1px solid ${t.colors.errorBorder}`,
        background: t.colors.errorBg,
        color: t.colors.errorText,
      };
    }

    return {
      ...base,
      border: `1px solid ${t.colors.infoBorder}`,
      background: t.colors.infoBg,
      color: t.colors.infoText,
    };
  },

  // Tables
  tableWrap: () => {
    const t = ui.tokens;
    return {
      marginTop: 12,
      overflowX: "auto",
      border: `1px solid ${t.colors.border}`,
      borderRadius: t.radius.lg,
      background: t.colors.surface,
    };
  },

  table: { width: "100%", borderCollapse: "collapse" },

  th: () => {
    const t = ui.tokens;
    return {
      textAlign: "left",
      fontSize: t.font.size.xs,
      color: t.colors.muted,
      background: t.colors.tableHeadBg,
      borderBottom: `1px solid ${t.colors.border}`,
      padding: "12px 10px",
      whiteSpace: "nowrap",
    };
  },

  td: () => {
    const t = ui.tokens;
    return {
      padding: "12px 10px",
      borderBottom: `1px solid ${t.colors.rowBorder}`,
      fontSize: t.font.size.sm,
      color: t.colors.text,
      whiteSpace: "nowrap",
    };
  },

  tdSmall: () => {
    const t = ui.tokens;
    return {
      padding: "10px 8px",
      borderBottom: `1px solid ${t.colors.rowBorder}`,
      verticalAlign: "top",
      fontSize: t.font.size.xs,
      color: t.colors.text,
      whiteSpace: "nowrap",
    };
  },

  // Modal
  overlay: () => {
    const t = ui.tokens;
    return {
      position: "fixed",
      inset: 0,
      background: t.colors.overlay,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: 16,
      zIndex: t.z.modal,
      overflow: "auto",
    };
  },

  modal: () => {
    const t = ui.tokens;
    return {
      width: "min(920px, 100%)",
      maxHeight: "min(88vh, 760px)",
      background: t.colors.surface,
      borderRadius: t.radius.xl,
      border: `1px solid ${t.colors.border}`,
      boxShadow: t.shadow.modal,
      overflow: "hidden",
      display: "flex",
      flexDirection: "column",
    };
  },

  modalHeader: () => {
    const t = ui.tokens;
    return {
      padding: "14px 16px",
      borderBottom: `1px solid ${t.colors.border}`,
      background: t.colors.headerBg,
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      gap: 12,
    };
  },

  modalBody: () => {
    const t = ui.tokens;
    return {
      padding: 16,
      overflow: "auto",
      flex: 1,
      background: t.colors.surface,
    };
  },

  // Info blocks
  infoGrid: { display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 12 },

  infoBox: () => {
    const t = ui.tokens;
    return {
      border: `1px solid ${t.colors.border}`,
      borderRadius: t.radius.md,
      padding: 12,
      background: t.colors.surface2,
    };
  },

  infoLabel: () => {
    const t = ui.tokens;
    return { fontSize: t.font.size.xs, color: t.colors.subtle };
  },

  infoValue: () => {
    const t = ui.tokens;
    return {
      fontSize: t.font.size.md,
      marginTop: 4,
      color: t.colors.text,
      fontWeight: t.font.weight.semibold,
    };
  },


// Adicionar no ui.js

emptyState: (opts = {}) => ({
  border: "1px dashed #e2e8f0",
  borderRadius: 14,
  padding: 16,
  background: "#fff",
  color: "#475569",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  gap: 10,
  ...opts,
}),

spinner: () => ({
  width: 14,
  height: 14,
  borderRadius: 999,
  border: "2px solid #cbd5e1",
  borderTopColor: "#2563eb",
  animation: "spin 0.9s linear infinite",
}),

section: () => ({
  marginTop: 14,
  padding: 14,
  border: "1px solid #e2e8f0",
  borderRadius: 14,
  background: "#fff",
}),

sectionHeader: () => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: 10,
  marginBottom: 10,
}),

fieldTitle: () => ({
  fontSize: 12,
  color: "#475569",
  fontWeight: 700,
  marginBottom: 6,
}),

box: () => ({
  border: "1px solid #e2e8f0",
  borderRadius: 12,
  padding: 12,
  background: "#fff",
  whiteSpace: "pre-wrap",
  color: "#0f172a",
}),

actionRow: (opts = {}) => ({
  display: "flex",
  alignItems: "end",
  justifyContent: "space-between",
  gap: 12,
  flexWrap: "wrap",
  ...opts,
}),

actionGroup: () => ({
  display: "grid",
  gap: 6,
  minWidth: 280,
}),

hint: () => ({
  fontSize: 12,
  color: "#64748b",
}),

errorText: () => ({
  fontSize: 12,
  color: "#b91c1c",
  fontWeight: 700,
}),



};

