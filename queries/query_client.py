TABLE_CLIENT = "client"

# Retorna a listagem de clientes com seus respectivos nomes, e-mails
# e o setor ao qual pertencem através do vínculo com a tabela 'sector'.
DISPLAY_CLIENTS_SQL = f"""
SELECT client.id, client.name, email, sector.name as sector
FROM client
JOIN sector ON client.id_sector = sector.id; 
"""
# Lista todos os chamados de um cliente específico, detalhando o técnico
# responsável (se houver), status, categoria e as descrições fornecidas pelo usuário.
DISPLAY_TICKETS_CLIENT_SQL = """
SELECT 
    t.id AS ticket_id,
    s.name AS support_name,
    t.status AS ticket_status,
    cat.name AS category_name,
    cat.descript AS problem_description,
    t.subject as subject_user,
    t.description as description_user
FROM ticket t
JOIN client c ON t.id_client = c.id
LEFT JOIN support_team s ON t.id_support = s.id
JOIN problem_categories cat ON t.id_problem_categories = cat.id
WHERE c.id = %s;"""
