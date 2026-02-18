class Messages:
    # ----------------------------------------------------------------------------
    # menus
    MENU_INITIAL = """
==============================
      SISTEMA DE CONSULTA
==============================
1. Logar como Cliente
2. Logar como Suporte
3. Sair
------------------------------ """

    MENU_CLIENT = """
1 - Ver meus tickets
2 - Buscar por ticket
3 - Criar um ticket
4 - Logout
"""

    MENU_JUNIOR_MID = """
1 - Ver meus tickets
2 - Resolver/cancelar ticket
3 - Logout
"""

    MENU_SENIOR_ENGINEER = """
1 - Ver meus tickets
2 - Buscar por ticket
3 - Resolver/cancelar tickets
4 - Ver todos os tickets em andamento
5 - Ver todos os tickets resolvidos, abertos ou cancelados
6 - Reatribuir ticket
7 - Logout
"""

    MENU_SEARCH_FLOW = """
Escolha uma das opções:
1 - Buscar por ID
2 - Buscar por texto
3 - Voltar
"""

    CHOICE_STATUS = """
escolha um status:
1 - Aberto
2 - Em progresso
3 - Resolvido
4 - Cancelado
            """

    CHOICE_YES_NOT = """Deseja colocar o status? (1)sim | (2)não """

    # ----------------------------------------------------------------------------

    # Title
    TIME_SUPPORT = "TIME DE SUPORTE: "
    ALL_TICKETS_OPEN = "TODOS OS TICKETS ABERTOS"
    YOUR_TICKETS_OPEN = "SEUS TICKETS ABERTOS"
    CHANGE_STATUS = "MUDANDO STATUS DO CHAMADO"
    # WARNINGS
    NO_ACTIVE_TICKETS = "Não há chamados em progresso."
    ONLY_OWN_TICKETS = "ATENÇÃO: Você só pode alterar tickets atribuídos a você."
    TICKET_REASSIGNED = "Ticket reatribuído com sucesso."
    NO_SUPPORT_AVAILABLE = "Suporte não disponível no momento."
    INPUT_CHANGE_STATUS = "Digite a mudança do status: " + "(1)resolved (2)cancel "
    INPUT_CHOICE_STATUS = (
        "Digite o status que deseja vizualizar: "
        + "(1)resolved (2)open (3)canceled (4)TODOS "
    )
    INPUT_ID_SUPPORT = "Digite o ID do supporte"
    NEW_OWNER_TICKET = "Novo responsável da ticket:"
    CHOICE_OPTIONS = "Escolha uma das opções: "
    TICKET_WILL_SWAPPED = "Ticket que vai ser trocada:"
    STATUS_INVALID = "opção do status invalida, escolha 1 ou 2"
    MENSAGE_COD_101 = (
        "Caso não encontre, digite 101 para você mesmo descrever o problema "
    )

    # MESSAGES
    MESSAGE_NOT_FOUND_TICKET = "Nenhum ticket encontrado"
    MESSAGE_SUJECT = "Digite o seu problema em poucas palavras: "
    MESSAGE_DESCRIPT = "Agora nos forneça o maximo de detalhes: "
    MESSAGE_ID_INVALID = "Digite o seu ID, deve ser numeros."
    MESSAGE_NOT_TICKET_PROGRESS = "Você não possui tickets em aberto."
    WRITE_ID = "Digite o id: "
    SEARCH_TEXT = "Busque seu ticket: "
    CHANGE_SUCCESS = "Trocado com sucesso"

    # ERRORS
    INVALID_OPTION = "Opção inválida. Escolha uma das opções do menu."
    NOT_FOUND_NO_SESSION = "Não foi encontrado o session"

    # ----------------------------------------------------------------------------

    # ALL PROGRAM
    ID_NOT_FOUND = "ID não encontrado."
    TICKET_NOT_FOUND = "ID do ticket não encontrado ou inválido."

    ID_NOT_FOUND_OR_INACTIVE = "ID não encontrado ou Usuário esta inativo."

    ERROR = "ERROR: "

    MESSAGE_GOOGBYE = "Até a Próxima ;)"
