from src.mensages import Messages
from src.client_table.client_actions import ClientActions
from src.enum.ticket_result import Tickets_results
from search.search_flow import SearchFlow


class Client_menu:

    def __init__(self) -> None:
        self.searchflow = SearchFlow()
        self.client = ClientActions()

    def menu_client(self, session):

        options = {
            "1": lambda: self.client.display_ticket_by_client(session.id_user),
            "2": lambda: self.searchflow.menu_search(session),
            "3": lambda: self.client.open_ticket(session.id_user),
            "4": "logout",
        }

        while True:
            print(Messages.MENU_CLIENT)
            option_user = self.client.requiered_option()

            if option_user == Tickets_results.INVALID_OPTION:
                print(Messages.INVALID_OPTION)
                continue

            action = options.get(option_user)

            if action == "logout":
                print(Messages.MESSAGE_GOOGBYE)
                break

            if action:
                result = action()

            if result == Tickets_results.ERROR:
                print(Messages.ERROR)
                continue
            continue
