class Queries:
    TABLE_SUPPORT = "support_team"
    TABLE_TICKET = "ticket"
    TABLE_SECTOR = "sector"
    TABLE_POSITION_COMPANY = "position_company"

    # criar um chamado (usuário)
    CREATE_TICKET_SQL = f"""
    INSERT INTO ticket
    (id_client, id_support, id_problem_categories, status, create_date)
    VALUES (%s, %s, %s, %s, %s) """

    # SELECTS
    CATEGORIES_PROBLEMS_SQL = f"""
    SELECT name, required_level FROM problems_categories
        """
    # Insere um novo chamado de suporte no banco de dados, registrando o cliente,
    # a categoria do problema, o status inicial e os detalhes da solicitação.
    CREATE_TICKET_FRONT_SQL = """
        INSERT INTO ticket
        (id_client, id_support, id_problem_categories, status, create_date, subject, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
