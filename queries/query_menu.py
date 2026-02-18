# Busca as informações básicas de identificação (ID e Nome) de um cliente específico.
GET_DATA_CLIENT_SQL = f"""
SELECT id, name FROM client WHERE id = %s;
"""

# Recupera os dados de um técnico de suporte, garantindo que o colaborador
# esteja com o cadastro ativo no sistema.
GET_DATA_SUPPORT_SQL = f"""
SELECT id, name, position_team
FROM support_team 
WHERE id = %s AND active_inactive = 1;
"""
