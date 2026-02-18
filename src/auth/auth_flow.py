from src.mensages import Messages
from src.utils import Utils
from src.auth.auth_services import AuthService
from src.session import Session


class AuthFlow:
    def __init__(self) -> None:
        self.utils = Utils()
        self.authservice = AuthService()
        self.session = Session()

    def get_option_user(self):
        choice = input(Messages.CHOICE_OPTIONS).strip()
        if choice not in ["1", "2", "3"]:
            return None
        return choice

    def display_menu_initial(self):
        print(Messages.MENU_INITIAL)

    def run(self):
        while True:
            self.session.logout()
            self.display_menu_initial()

            choice = self.get_option_user()

            if choice == "3":
                break

            if choice not in ["1", "2"]:
                print(Messages.INVALID_OPTION)
                continue

            id_user = self.utils.requests_id()
            if not id_user:
                print(Messages.MESSAGE_ID_INVALID)
                continue

            user_data = self.authservice.get_data_by_id(choice, id_user)

            if not user_data:
                print(Messages.ID_NOT_FOUND_OR_INACTIVE)
                continue

            role, id_, name, position_team = user_data

            self.session.keep_data(role, id_, name, position_team)

            self._redirect_user(role)

    def _redirect_user(self, role):
        if role == "client":
            from src.client_table.client_menu import Client_menu

            Client_menu().menu_client(self.session)

        elif role == "support":
            from src.support.support_menu import MenuSupport

            MenuSupport().looping_menu_support(self.session)
