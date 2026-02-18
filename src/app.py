# classes
from src.auth.auth_flow import AuthFlow
from src.client_table.client_actions import ClientActions
from src.support.support_menu import MenuSupport


client = ClientActions()
menu_support = MenuSupport()
authflow = AuthFlow()


class App:

    def init_menu(self):
        authflow.run()
