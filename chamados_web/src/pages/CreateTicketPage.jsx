import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { useNavigate } from "react-router-dom";
import { ui } from "../ui/ui";

const OTHER_CATEGORY_ID = 101;

export default function CreateTicketPage() {
  const navigate = useNavigate();
  const t = ui.tokens;

  const [categories, setCategories] = useState([]);
  const [categoryId, setCategoryId] = useState("");
  const [subject, setSubject] = useState("");
  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const selectedCategory = useMemo(
    () => categories.find((c) => String(c.id) === String(categoryId)),
    [categories, categoryId]
  );

  const isOther = Number(categoryId) === OTHER_CATEGORY_ID;

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setErrorMsg("");

      try {
        const res = await api.get("/tickets/problem-categories");
        if (cancelled) return;

        setCategories(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        const detail = err?.response?.data?.detail;
        if (!cancelled) setErrorMsg(detail || "Erro ao carregar categorias.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!categoryId) {
      setErrorMsg("Selecione uma categoria.");
      return;
    }

    const cid = Number(categoryId);
    const subjectTrim = subject.trim();
    const descTrim = description.trim();

    if (cid === OTHER_CATEGORY_ID && (!subjectTrim || !descTrim)) {
      setErrorMsg("Para 'Não encontrei', informe assunto e descrição.");
      return;
    }

    setSaving(true);
    setErrorMsg("");

    try {
      const payload = { category_id: cid };
      if (subjectTrim) payload.subject = subjectTrim;
      if (descTrim) payload.description = descTrim;

      await api.post("/tickets", payload);
      navigate("/home");
    } catch (err) {
      const detail = err?.response?.data?.detail;
      setErrorMsg(detail || `Erro ao criar ticket. (${err?.response?.status || "?"})`);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={{ ...ui.page, maxWidth: 900 }}>
      {/* HEADER */}
      <div style={ui.headerRow(t)}>
        <div>
          <h1 style={ui.title(t)}>Criar ticket</h1>
          <p style={ui.subtitle(t)}>
            Selecione uma categoria e descreva o problema para abrir o chamado.
          </p>
        </div>

        <div style={ui.toolbar}>
          <button style={ui.button("secondary")} type="button" onClick={() => navigate("/home")}>
            Voltar
          </button>
        </div>
      </div>

      {/* CONTENT */}
      <div style={ui.card(t)}>
        {errorMsg ? <div style={ui.alert("error")}>{errorMsg}</div> : null}

        {loading ? (
          <div style={ui.emptyState({ marginTop: 12 })}>
            <div style={ui.spinner()} />
            <div>Carregando categorias...</div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: "grid", gap: 14, marginTop: 12 }}>
            {/* Categoria */}
            <div style={ui.section()}>
              <div style={ui.sectionHeader()}>
                <h3 style={ui.sectionTitle(t)}>Categoria</h3>
              </div>

              <label style={ui.label(t)}>
                Selecione
                <select
                  value={categoryId}
                  onChange={(e) => setCategoryId(e.target.value)}
                  style={ui.select(t)}
                  disabled={saving}
                >
                  <option value="">Selecione</option>
                  {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </label>

              {/* regra 101 */}
              {isOther ? (
                <div style={{ marginTop: 10, ...ui.alert("info") }}>
                  Para essa categoria, <b>Assunto</b> e <b>Descrição</b> são obrigatórios.
                </div>
              ) : null}

              {/* descrição da categoria */}
              <div style={{ marginTop: 10 }}>
                <div style={ui.fieldTitle()}>Descrição da categoria</div>
                <div style={ui.hint()}>
                  {selectedCategory?.description
                    ? selectedCategory.description
                    : "Selecione uma categoria para ver a descrição."}
                </div>
              </div>
            </div>

            {/* Detalhes */}
            <div style={ui.section()}>
              <div style={ui.sectionHeader()}>
                <h3 style={ui.sectionTitle(t)}>Detalhes</h3>
              </div>

              <div style={{ display: "grid", gap: 12 }}>
                <label style={ui.label(t)}>
                  Assunto
                  <input
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    style={ui.input(t)}
                    disabled={saving}
                    placeholder={isOther ? "Obrigatório para 'Não encontrei'" : "Opcional"}
                  />
                </label>

                <label style={ui.label(t)}>
                  Descrição
                  <textarea
                    rows={5}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    style={ui.textarea(t)}
                    disabled={saving}
                    placeholder={isOther ? "Obrigatória para 'Não encontrei'" : "Descreva o problema (opcional)"}
                  />
                </label>
              </div>
            </div>

            {/* Actions */}
            <div style={ui.actionRow()}>
              <div style={ui.hint()}>
                Ao criar, você será redirecionado para a Home.
              </div>

              <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                <button
                  type="button"
                  style={ui.button("secondary")}
                  onClick={() => navigate("/home")}
                  disabled={saving}
                >
                  Cancelar
                </button>

                <button type="submit" style={ui.button("primary")} disabled={saving || !categoryId}>
                  {saving ? "Criando..." : "Criar ticket"}
                </button>
              </div>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
