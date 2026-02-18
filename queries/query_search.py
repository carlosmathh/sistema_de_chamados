# Busca os detalhes completos de um ticket específico vinculado a um cliente,
# garantindo que o cliente autenticado só acesse seus próprios chamados.
SEARCH_BY_ID_CLIENT = """
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
WHERE t.id = %s
    AND t.id_client = %s

"""

# Realiza a busca detalhada de um ticket de um cliente filtrando também pelo status,
# útil para validações de fluxo de trabalho no frontend.
SEARCH_BY_ID_CLIENT_STATUS = """
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
WHERE t.id = %s
    AND t.id_client = %s
    AND t.status = %s
"""

# Consulta as informações globais de um ticket pelo ID para a visão da equipe de suporte,
# permitindo visualizar dados do cliente, categoria e técnico atribuído.
SEARCH_BY_ID_SUPPORT = """
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
WHERE t.id = %s;
"""

# Recupera os detalhes de um ticket filtrando por ID e status, permitindo que a
# equipe de suporte valide o estado atual do chamado antes de realizar ações.
SEARCH_BY_ID_SUPPORT_STATUS = """
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
WHERE t.id = %s
    AND t.status = %s;
"""

# Realiza uma busca textual nos chamados de um cliente, filtrando pelo nome
# da categoria ou pelo assunto, para facilitar a localização de tickets antigos.
SEARCH_FOR_TEXT_CLIENT = """
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
  AND (pc.name LIKE %s OR t.subject LIKE %s);
"""

# Combina a busca textual (categoria ou assunto) com um filtro de status específico,
# refinando a listagem de chamados para o painel do cliente.
SEARCH_FOR_TEXT_CLIENT_STATUS = """
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
  AND (pc.name LIKE %s OR t.subject LIKE %s)
  AND t.status = %s;
"""

# Permite que a equipe de suporte localize chamados em toda a base de dados
# através de busca textual pelo nome da categoria ou pelo assunto do ticket.
SEARCH_FOR_TEXT_SUPPORT = """
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
WHERE (pc.name LIKE %s OR t.subject LIKE %s)
"""

# Realiza a busca textual filtrando simultaneamente por um status específico,
# ideal para o suporte encontrar rapidamente problemas pendentes ou finalizados.
SEARCH_FOR_TEXT_SUPPORT_STATUS = """
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
WHERE (pc.name LIKE %s OR t.subject LIKE %s)
  AND t.status = %s;
"""
