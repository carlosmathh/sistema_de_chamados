from src.utils import Utils
from src.mensages import Messages
from src.enum.ticket_result import Tickets_results
from src.support.support_services import SupportServices
from src.support.support_flow import SupportFlow
from search.search_flow import SearchFlow
from db.connection import get_connection
from src.audit.ticket_history_service import TicketHistoryService


class MenuSupport:
    # ----------------------------------------------------------------------------------------
    # MENU LOOPING

    def __init__(self) -> None:
        conn = get_connection()
        self.utils = Utils()
        tickethistory = TicketHistoryService()

        self.flow = SupportFlow(conn, self.utils, tickethistory)
        self.searchflow = SearchFlow()
        self.services = SupportServices(conn, self.utils, tickethistory)

    def show_uni_support_active_tickets(self, id_support):
        datas = self.services.get_uni_support_active_tickets(id_support)
        print(Messages.YOUR_TICKETS_OPEN)
        self.utils.display_list(
            list(datas),
            "id",
            "category_name",
            "descript",
            "base_complexity",
            "subject",
            "descrit_user",
        )
        if not datas:
            return None

    def show_all_active_tickets(self):
        print(Messages.ALL_TICKETS_OPEN)
        datas = self.services.get_all_active_tickets()

        self.utils.display_list(
            list(datas),
            "id",
            "id_support",
            "support_name",
            "category_name",
            "r_level",
        )
        return datas

    def show_tickets_open_resolved_cancel(self):
        datas = self.flow.get_user_choice_open_resolved_cancel()

        if isinstance(datas, list):
            self.utils.display_list(
                datas,
                "id",
                "status",
                "create_date",
                "resolution_date",
                "client_name",
                "category_name",
                "required_level",
                "support_name",
            )
        else:
            print(datas)

    def run_menu(self, menu, actions, exit):

        while True:
            print(menu)
            option_user = input(Messages.CHOICE_OPTIONS)
            if option_user == exit:
                print(Messages.MESSAGE_GOOGBYE)
                break
            action = actions.get(option_user)
            if not action:
                print(Messages.INVALID_OPTION)
                continue
            if not actions:
                print(Messages.INVALID_OPTION)
                continue

            action()

        return ""

    def handle_change_status(self, id_):
        print(Messages.CHANGE_STATUS)
        print()
        has_tickets = self.show_uni_support_active_tickets(id_)
        if has_tickets == None:
            return

        result = self.flow.change_status(id_)

        if result == Tickets_results.NO_ACTIVE_TICKETS:
            print(Messages.NO_ACTIVE_TICKETS)
        elif result == Tickets_results.NOT_OWNER:
            print(Messages.ONLY_OWN_TICKETS)
        elif result == Tickets_results.INVALID_STATUS:
            print(Messages.STATUS_INVALID)
        elif result == Tickets_results.SUCCESS:
            print(Messages.CHANGE_SUCCESS)
        elif result == Tickets_results.ERROR:
            print(Messages.ERROR)

    def handle_reassign_ticket(self):
        self.show_all_active_tickets()
        print(Messages.TICKET_WILL_SWAPPED)

        result = self.flow.reassign_ticket(self.id_support_init)

        if result == Tickets_results.NO_ACTIVE_TICKETS:
            print(Messages.NO_ACTIVE_TICKETS)
        elif result == Tickets_results.NOT_FOUND:
            print(Messages.ID_NOT_FOUND)
        elif result == Tickets_results.NO_AVAILABLE:
            print(Messages.NO_SUPPORT_AVAILABLE)
        elif result == Tickets_results.NOT_SUPPORT_FOUND:
            print(Messages.ID_NOT_FOUND)
        elif result == Tickets_results.SUCCESS:
            print(Messages.CHANGE_SUCCESS)
        elif result == Tickets_results.ERROR:
            print(Messages.ERROR)

    def run_low_position_menu(self, id_):
        actions = {
            "1": lambda: self.show_uni_support_active_tickets(id_),
            "2": lambda: self.handle_change_status(id_),
        }
        self.run_menu(Messages.MENU_JUNIOR_MID, actions, "3")

    def run_high_position_menu(self, session, id_):
        actions = {
            "1": lambda: self.show_uni_support_active_tickets(id_),
            "2": lambda: self.searchflow.menu_search(session),
            "3": lambda: self.handle_change_status(id_),
            "4": self.show_all_active_tickets,
            "5": self.show_tickets_open_resolved_cancel,
            "6": self.handle_reassign_ticket,
        }
        self.run_menu(Messages.MENU_SENIOR_ENGINEER, actions, "7")

    # looping do menu support
    def looping_menu_support(self, session):

        if not session.is_active():
            print(Messages.NOT_FOUND_NO_SESSION)
            return

        self.id_support_init = session.id_user
        position_team = session.position_team

        if position_team in ("junior", "mid_level"):
            self.run_low_position_menu(self.id_support_init)
        elif position_team in ("senior", "engineer"):
            self.run_high_position_menu(session, self.id_support_init)
        else:
            return None
