# Registra uma nova entrada na trilha de auditoria (log) de um chamado,
# documentando mudanças de estado, quem realizou a ação e observações adicionais.
INSERT_HISTORY_SQL = """
INSERT INTO ticket_history (
    id_ticket,
    event_type,
    old_value,
    new_value,
    actor_type,
    actor_id,
    note
) VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Recupera o histórico completo de eventos de um chamado específico,
# ordenado do mais recente para o mais antigo para visualização da timeline.
LIST_TICKET_HISTORY_SQL = """
SELECT
  id,
  id_ticket AS ticket_id,
  event_type,
  old_value,
  new_value,
  actor_type,
  actor_id,
  created_at,
  note
FROM ticket_history
WHERE id_ticket = %s
ORDER BY created_at DESC, id DESC;

"""
