import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom";
import { ui } from "../ui/ui";

export default function LoginPage() {
  const { loginWithToken, isAuthed } = useAuth();
  const navigate = useNavigate();
  const t = ui.tokens;


  const [role, setRole] = useState("client");
  const [userId, setUserId] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    if (isAuthed) navigate("/home", { replace: true });
  }, [isAuthed, navigate]);

  async function handleLogin(e) {
    e.preventDefault();
    setErrorMsg("");
    setLoading(true);

    try {
      const idNum = Number(userId);
      if (!Number.isInteger(idNum) || idNum <= 0) {
        throw new Error("ID inválido.");
      }

      const res = await api.post("/auth/login", { role, id: idNum });

      const token = res.data?.access_token;
      if (!token) throw new Error("Token não retornado.");

      loginWithToken(token);
    } catch (err) {
      setErrorMsg(
        err?.response?.data?.detail || err?.message || "Erro ao logar. Confira role e id."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        padding: 16,
        fontFamily: t.font.sans,
        color: t.colors.text,
      }}
    >


      <div style={{ width: "min(520px, 100%)" }}>
        

        {/* Branding */}
        <div style={{ marginBottom: 14 }}>
          <div style={{ fontSize: t.font.size.xs, color: t.colors.subtle, fontWeight: t.font.weight.bold }}>
            Chamado Ágil
          </div>
          <h1 style={{ margin: "6px 0 0", fontSize: t.font.size["2xl"], letterSpacing: t.font.tracking.tight }}>
            Entrar no sistema
          </h1>
          <p style={{ margin: "8px 0 0", color: t.colors.muted, fontSize: t.font.size.sm }}>
            Acesse para criar, acompanhar e gerenciar chamados.
          </p>
        </div>

        {/* Card */}
        <div style={{ ...ui.card(t), marginTop: 0 }}>
          <form onSubmit={handleLogin} style={{ display: "grid", gap: 12 }}>
            <div style={{ display: "grid", gap: 10 }}>
              <label style={ui.label(t)}>
                Perfil
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  style={ui.select(t)}
                  disabled={loading}
                >
                  <option value="client">Cliente</option>
                  <option value="support">Suporte</option>
                </select>
              </label>

              <label style={ui.label(t)}>
                ID
                <input
                  value={userId}
                  onChange={(e) => setUserId(e.target.value)}
                  placeholder="Ex: 15"
                  style={ui.input(t)}
                  disabled={loading}
                />
              </label>
            </div>

            <button
              type="submit"
              style={ui.button("primary")}
              disabled={loading || !userId.trim()}
            >
              {loading ? "Entrando..." : "Entrar"}
            </button>

            {errorMsg ? <div style={ui.alert("error")}>{errorMsg}</div> : null}

            <div style={{ marginTop: 2, fontSize: t.font.size.xs, color: t.colors.subtle }}>
              Dica: use seu ID de <b>cliente</b> ou <b>suporte</b> conforme configurado no backend.
            </div>
          </form>
        </div>

        {/* Footer sutil */}
        <div style={{ marginTop: 12, textAlign: "center", fontSize: t.font.size.xs, color: t.colors.subtle }}>
          © {new Date().getFullYear()} Chamado Ágil  • v0.1
        </div>
      </div>
    </div>
  );
}
