# classes
from src.auth.auth_flow import AuthFlow
from src.client_table.client_actions import ClientActions
from src.support.support_menu import MenuSupport


client = ClientActions()
menu_support = MenuSupport()
authflow = AuthFlow()


class App:

    # def client_open_ticket(self):
    #     client.open_ticket()

    # def alter_ticket_by_support(self):
    #     menu_support.looping_menu_support()

    def init_menu(self):
        authflow.run()
