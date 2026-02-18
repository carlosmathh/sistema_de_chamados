# SELECTS -------------------------------------------


# mostra o id e quantidade de ticket de cada support
SHOW_POSITION_TEAM_SQL = f"""
SELECT
	support_team.id,
	count(ticket.id) AS total
FROM support_team
LEFT JOIN ticket ON ticket.id_support = support_team.id
	AND ticket.status IN ('open', 'in_progress')
WHERE  support_team.position_team = (%s)
	AND support_team.active_inactive = 1
GROUP BY support_team.id, support_team.name
HAVING total < 3
ORDER BY total ASC
"""

# SÓ SENNOR OU ENGINEER PODE USA-LO
# MOSTRA TODOS TICKETS EM ANDAMENTO
SHOW_ALL_TICKETS_PROGRESS_SQL = f"""
SELECT 
    t.id, 
    t.id_support, 
    s.name AS support_name, 
    c.name AS category_name,
    c.required_level as r_level
FROM ticket AS t
JOIN support_team AS s ON t.id_support = s.id
JOIN problem_categories AS c ON t.id_problem_categories = c.id
WHERE t.status = 'in_progress';
"""

# RETORNA SUPPORTS VALIDOS PARA RECEBER UMA TRANSFERENCIA DE TICKET
GET_TICKET_COMFIRM_SQL = f"""
SELECT id
from ticket 
WHERE ticket.id = %s
"""


# VERIFICAA E RETORNA SE SUPPORT É VALIDO PARA RECEBER UMA
#  TRANSFERENCIA DE TICKET
GET_SUPPORTS_AVAILABLE_SQL = f"""
SELECT 
    s.id,
    s.name,
    COUNT(t.id) AS total_tickets
FROM support_team AS s
LEFT JOIN ticket AS t 
    ON s.id = t.id_support
   AND t.status = 'in_progress'
WHERE 
    s.id = %s               -- id_new_owner
    AND s.active_inactive = 1
    AND s.position_team >= %s -- required_level
GROUP BY s.id, s.name, s.position_team
HAVING COUNT(t.id) < 3;

"""

# Lista técnicos disponíveis que possuem nível técnico igual ou superior ao solicitado,
# limitando a busca a profissionais ativos e com menos de 3 chamados em andamento.
LIST_AVAILABLE_SUPPORTS_SQL = """
SELECT
  s.id,
  s.name,
  s.position_team,
  COUNT(t.id) AS in_progress_count
FROM support_team AS s  
LEFT JOIN ticket AS t
  ON s.id = t.id_support
 AND t.status = 'in_progress'
WHERE
  s.active_inactive = 1
  AND s.position_team >= %s
GROUP BY s.id, s.name, s.position_team
HAVING COUNT(t.id) < 3
ORDER BY in_progress_count ASC, s.position_team ASC, s.id ASC;
"""

# (Frontend) Identifica técnicos elegíveis para assumir um ticket específico, comparando
# o nível do técnico com o nível exigido pela categoria do chamado (subquery).
# Filtra apenas técnicos com menos de 3 tickets ativos para evitar sobrecarga.
LIST_AVAILABLE_SUPPORTS_FRONT_SQL = """
SELECT
  s.id,
  s.name,
  s.position_team,
  COUNT(t.id) AS in_progress_count
FROM support_team s
LEFT JOIN ticket t
  ON s.id = t.id_support
 AND t.status = 'in_progress'
WHERE s.active_inactive = 1
  AND (s.position_team + 0) >= (
    SELECT (pc.required_level + 0)
    FROM ticket tk
    JOIN problem_categories pc ON pc.id = tk.id_problem_categories
    WHERE tk.id = %s
  )
GROUP BY s.id, s.name, s.position_team
HAVING COUNT(t.id) < 3
ORDER BY in_progress_count ASC, (s.position_team + 0) ASC, s.id ASC;
"""


# RETORNA UM TICKET DE UM SUPPORT
GET_SUPPORT_SPECIFY = f"""
SELECT 
    t.id_support,
    c.required_level AS level
FROM ticket AS t
JOIN support_team AS s ON t.id_support = s.id
JOIN problem_categories AS c ON t.id_problem_categories = c.id
WHERE t.id = %s
    AND t.status = 'in_progress';
"""


# RETONA O ID DE UM UNICO TICKET
GET_UNI_TICKETS_PROGRESS_SQL = f"""
SELECT 
    id 
FROM ticket 
WHERE status = 'in_progress' 
  AND id_support = %s;
"""
# Recupera a lista detalhada de chamados em andamento (in_progress) atribuídos
# a um técnico específico, incluindo informações da categoria para facilitar a triagem.
GET_TICKETS_PROGRESS = f"""
SELECT 
    t.id, 
    pc.name as category_name, 
    pc.descript, 
    pc.base_complexity, 
    t.subject, 
    t.description AS descrit_user
FROM 
    ticket AS t
INNER JOIN 
    problem_categories AS pc 
ON 
    t.id_problem_categories = pc.id
WHERE 
    t.id_support = %s 
    AND t.status = 'in_progress';
"""

# Valida se um ticket específico pertence ao técnico atual e se ainda está
# em um estado editável ('open' ou 'in_progress') antes de permitir alterações.
VALIDATE_TICKET_OWNER_SQL = """
SELECT id
FROM ticket
WHERE id = %s
  AND id_support = %s
  AND status IN ('open', 'in_progress');
"""


# MOSTRA TODO TIME DE SUPPORT
SHOW_ALL_SUPPORT_TEAM_SQL = f"""
SELECT id, name, position_team
FROM support_team
"""

# (Frontend) Lista todos os chamados com um status específico, trazendo os dados
# consolidados de cliente, categoria e técnico, ordenados pela data de criação
# (do mais antigo para o mais recente) para controle de fila.
SHOW_TICKET_STATUS_SPECIFY_FRONT_SQL = f"""
SELECT 
    t.id AS ticket_id,
    t.status,
    t.create_date,
    t.resolution_date,
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    s.name AS support_name
FROM ticket AS t
INNER JOIN client AS c ON c.id = t.id_client 
INNER JOIN problem_categories AS pc ON pc.id = t.id_problem_categories 
LEFT JOIN support_team AS s ON s.id = t.id_support 
WHERE t.status = (%s)
ORDER BY t.create_date ASC;

"""

# MOSTRA TODOS TICKETS COM STATUS OPEN, RESOLVED OU CANCELED
SHOW_TICKET_STATUS_SPECIFY_SQL = f"""
SELECT 
    t.id,
    t.status,
    t.create_date,
    t.resolution_date, -- Se for NULL, o SQL retorna NULL normalmente
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    s.name AS support_name -- Retornará NULL se não houver técnico vinculado
FROM ticket AS t
INNER JOIN client AS c ON c.id = t.id_client 
INNER JOIN problem_categories AS pc ON pc.id = t.id_problem_categories 
LEFT JOIN support_team AS s ON s.id = t.id_support 
WHERE t.status = (%s)
ORDER BY t.create_date ASC;

"""


# MOSTRA TODOS TICKETS COM STATUS OPEN, RESOLVED, CANCELED e IN_PROGRESS
SHOW_TICKET_STATUS_ALL_SQL = f"""
SELECT 
    t.id,
    t.status,
    t.create_date,
    t.resolution_date, -- Se for NULL, o SQL retorna NULL normalmente
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    s.name AS support_name -- Retornará NULL se não houver técnico vinculado
FROM ticket AS t
INNER JOIN client AS c ON c.id = t.id_client 
INNER JOIN problem_categories AS pc ON pc.id = t.id_problem_categories 
LEFT JOIN support_team AS s ON s.id = t.id_support 
WHERE t.status in (%s,%s,%s,%s)
ORDER BY t.create_date ASC;

"""


# MOSTRA TODOS TICKETS COM STATUS OPEN, RESOLVED, CANCELED e IN_PROGRESS
SHOW_TICKET_STATUS_ALL_FRONT_SQL = f"""
SELECT 
    t.id,
    t.status,
    t.create_date,
    t.resolution_date, -- Se for NULL, o SQL retorna NULL normalmente
    c.name AS client_name,
    pc.name AS category_name,
    pc.required_level,
    s.name AS support_name -- Retornará NULL se não houver técnico vinculado
FROM ticket AS t
INNER JOIN client AS c ON c.id = t.id_client 
INNER JOIN problem_categories AS pc ON pc.id = t.id_problem_categories 
LEFT JOIN support_team AS s ON s.id = t.id_support 
WHERE t.status in (%s,%s,%s,%s)
ORDER BY t.create_date ASC;

"""


# UPDATE-------------------------------------------
# MUDA STATUS
RESOLVED_CANCEL_TICKET_SQL = f"""
UPDATE ticket
SET status = %s, resolution_date = %s
WHERE id = %s 
AND status IN ('open', 'in_progress')
"""

# Realiza a transferência de um chamado entre técnicos, garantindo que o ticket
# esteja em andamento e evitando processamento desnecessário caso o novo
# responsável seja igual ao atual.
REASSIGN_TICKET_SQL = """
UPDATE ticket 
SET id_support = %s
WHERE id = %s 
  AND status = 'in_progress'
  AND id_support != %s; -- Evita reatribuir para a mesma pessoa
"""

# (Frontend) Executa a reatribuição de um ticket validando se o novo técnico
# está ativo e se possui o nível técnico necessário (position_team) para a
# categoria do problema, além de garantir que o status permita a troca.
REASSIGN_TICKET_FRONT_SQL = """
UPDATE ticket tk
JOIN problem_categories pc ON pc.id = tk.id_problem_categories
JOIN support_team s ON s.id = %s
SET tk.id_support = %s
WHERE tk.id = %s
  AND tk.status = 'in_progress'
  AND tk.id_support != %s
  AND s.active_inactive = 1
  AND (s.position_team + 0) >= (pc.required_level + 0);
"""
