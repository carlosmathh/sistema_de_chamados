# Realiza a abertura de um novo chamado no sistema, salvando as referências
# do cliente, técnico, categoria e a descrição inicial do problema.
INSERT_TICKET_SQL = f"""
INSERT INTO ticket (    
    id_client,
    id_support,
    id_problem_categories,
    status,
    create_date,
    subject,
    description

)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Obtém a visão 360º de um ticket específico, unindo IDs e nomes de todas
# as entidades relacionadas (cliente, categoria e suporte) para exibição detalhada
GET_TICKET_DETAILS = """
SELECT
    t.id AS ticket_id,
    t.status,
    t.create_date,
    t.resolution_date,
    c.id AS client_id,
    c.name AS client_name,
    pc.id AS category_id,
    pc.name AS category_name,
    pc.required_level,
    st.id AS support_id,
    st.name AS support_name,
    t.subject AS subject_user,
    t.description AS description_user
FROM ticket t
LEFT JOIN client c ON t.id_client = c.id
LEFT JOIN problem_categories pc ON t.id_problem_categories = pc.id
LEFT JOIN support_team st ON t.id_support = st.id
WHERE t.id = %s
"""

# Atualiza o status do chamado e gerencia automaticamente a data de resolução:
# define como o momento atual se finalizado/cancelado, ou limpa se reaberto.
UPDATE_TICKET_STATUS = """
UPDATE ticket
SET status = %s,
    resolution_date = CASE
        WHEN %s IN ('resolved','canceled') THEN NOW()
        ELSE NULL
    END
WHERE id = %s
"""

# Consulta rápida para identificar qual técnico está atualmente
# responsável por um determinado ticket.
GET_TICKET_OWNER_SUPPORT = """
SELECT id_support
FROM ticket
WHERE id = %s
"""

# Recupera todos os chamados abertos por um cliente específico,
# ordenando dos mais recentes para os mais antigos.
GET_MY_TICKETS_CLIENT = """
SELECT
    t.id AS ticket_id,
    t.status,
    t.create_date,
    t.resolution_date,
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    st.name AS support_name,
    t.subject AS subject_user,
    t.description AS description_user
FROM ticket t
LEFT JOIN client c ON t.id_client = c.id
LEFT JOIN problem_categories pc ON t.id_problem_categories = pc.id
LEFT JOIN support_team st ON t.id_support = st.id
WHERE t.id_client = %s
ORDER BY t.create_date DESC
"""

# Lista os chamados de um cliente filtrados por um status específico (ex: apenas 'abertos'),
# mantendo a ordenação cronológica decrescente.
GET_MY_TICKETS_CLIENT_STATUS = """
SELECT
    t.id AS ticket_id,
    t.status,
    t.create_date,
    t.resolution_date,
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    st.name AS support_name,
    t.subject AS subject_user,
    t.description AS description_user
FROM ticket t
LEFT JOIN client c ON t.id_client = c.id
LEFT JOIN problem_categories pc ON t.id_problem_categories = pc.id
LEFT JOIN support_team st ON t.id_support = st.id
WHERE t.id_client = %s
  AND t.status = %s
ORDER BY t.create_date DESC
"""

# Retorna todos os chamados atribuídos a um técnico de suporte específico,
# fornecendo uma visão geral da carga de trabalho histórica e atual.
GET_MY_TICKETS_SUPPORT = """
SELECT
    t.id AS ticket_id,
    t.status,
    t.create_date,
    t.resolution_date,
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    st.name AS support_name,
    t.subject AS subject_user,
    t.description AS description_user
FROM ticket t
LEFT JOIN client c ON t.id_client = c.id
LEFT JOIN problem_categories pc ON t.id_problem_categories = pc.id
LEFT JOIN support_team st ON t.id_support = st.id
WHERE t.id_support = %s
ORDER BY t.create_date DESC
"""

# Filtra a lista de chamados de um técnico por status, permitindo que ele
# foque apenas nos tickets em que precisa atuar no momento (ex: 'em progresso').
GET_MY_TICKETS_SUPPORT_STATUS = """
SELECT
    t.id AS ticket_id,
    t.status,
    t.create_date,
    t.resolution_date,
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    st.name AS support_name,
    t.subject AS subject_user,
    t.description AS description_user
FROM ticket t
LEFT JOIN client c ON t.id_client = c.id
LEFT JOIN problem_categories pc ON t.id_problem_categories = pc.id
LEFT JOIN support_team st ON t.id_support = st.id
WHERE t.id_support = %s
  AND t.status = %s
ORDER BY t.create_date DESC
"""
