from src.mensages import Messages
from search.search_services import SearchServices
from src.utils import Utils
from db.connection import get_connection


class SearchFlow:

    def __init__(self) -> None:
        self.utils = Utils()
        self.conn = get_connection()
        self.search_services = SearchServices(self.conn)

    def display_search(self, data):
        if not data:
            print(Messages.TICKET_NOT_FOUND)
            return

        if isinstance(data, dict):
            data = [data]

        self.utils.display_list(
            data,
            "ticket_id",
            "status",
            "create_date",
            "resolution_date",
            "client_name",
            "category_name",
            "required_level",
            "support_name",
            "subject_user",
            "description_user",
        )

    # Pega o status ou None
    def get_status(self):
        status_user = None
        options = {"1": "sim", "2": "não"}
        choice = input(Messages.CHOICE_YES_NOT)

        choice_user = options.get(choice)

        if not choice_user:
            print(Messages.INVALID_OPTION)
            return

        if choice_user == "não":
            return

        status_options = {
            "1": "open",
            "2": "in_progress",
            "3": "resolved",
            "4": "canceled",
        }

        if choice_user == "sim":
            status = input(Messages.CHOICE_STATUS)

            if status not in ["1", "2", "3", "4"]:
                print(Messages.INVALID_OPTION)
                return

            status_user = status_options.get(status)
        return status_user

    # Pega id e status
    def get_data_ticket_by_id(self):
        ticket_id = input(Messages.WRITE_ID)

        status = self.get_status()
        try:
            id_ticket_int = int(ticket_id)
            if id_ticket_int <= 0:
                print(Messages.MESSAGE_ID_INVALID)
                return None
        except ValueError:
            print(Messages.MESSAGE_ID_INVALID)
            return None

        return (id_ticket_int, status)

    # Mostra na tela
    def display_ticket_by_id(self, session):
        tuple_data = self.get_data_ticket_by_id()

        if not tuple_data:
            return

        ticket_id, status = tuple_data

        data = self.search_services.search_ticket_by_id(
            user_role=session.role,
            ticket_id=ticket_id,
            client_id=session.id_user if session.role == "client" else None,
            status=status,
        )
        if not data:
            print(Messages.MESSAGE_NOT_FOUND_TICKET)
            return None

        self.display_search(data)

    def get_data_ticket_by_text(self):
        ticket_text = input(Messages.MESSAGE_SUJECT)
        status = self.get_status()
        return ticket_text, status

    def display_ticket_by_text(self, session):
        ticket_text, status = self.get_data_ticket_by_text()

        data = self.search_services.search_tickets_by_text(
            user_role=session.role,
            text=ticket_text,
            client_id=session.id_user if session.role == "client" else None,
            status=status,
        )

        if not data:
            print(Messages.MESSAGE_NOT_FOUND_TICKET)
            return None

        self.display_search(data)

    def menu_search(self, session):

        while True:
            print(Messages.MENU_SEARCH_FLOW)
            option_user = input(Messages.CHOICE_OPTIONS)

            actions = {
                "1": lambda: self.display_ticket_by_id(session),
                "2": lambda: self.display_ticket_by_text(session),
                "3": "voltar",
            }

            action = actions.get(option_user)

            if action == "voltar":
                return
            if not action:
                print(Messages.INVALID_OPTION)
                continue

            action()
