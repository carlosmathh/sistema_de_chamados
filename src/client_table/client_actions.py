from src.utils import Utils
from src.client_table.client_services import ClientServices
from src.assign_support import AssingSupport
from src.problem_categories import Problem_categories
from src.mensages import Messages
from src.enum.ticket_result import Tickets_results
from db.connection import get_connection


class ClientActions:
    def __init__(self) -> None:
        self.conn = get_connection()
        self.utils = Utils()

        self.problem_categories = Problem_categories(self.conn, self.utils)
        self.ticket = ClientServices(self.conn)
        self.assing_support = AssingSupport(self.conn, self.utils)

    def requiered_option(self):
        option = input(Messages.CHOICE_OPTIONS)
        if not option or option not in ["1", "2", "3", "4"]:
            return Tickets_results.INVALID_OPTION
        return option

    def display_ticket_by_client(self, id_client):
        datas = self.ticket.get_ticket_by_client(id_client)
        self.utils.display_list(
            datas,
            "ticket_id",
            "support_name",
            "ticket_status",
            "category_name",
            "problem_description",
            "subject_user",
            "description_user",
        )

    def open_ticket(self, id_client):
        # self.display_client()
        # id_client = self.id_in_list()

        defined_data = self.utils.define_date_now()

        self.problem_categories.display_problem_categories()
        id_, id_ticket = self.problem_categories.id_in_problem_categories()

        if id_ == "101":
            subject = input(Messages.MESSAGE_SUJECT)
            description = input(Messages.MESSAGE_DESCRIPT)
        else:
            subject = None
            description = None

        id_support = self.assing_support.assign_support(id_ticket)

        if id_support != None:
            status = "in_progress"
            print("“Ticket criado”")
        else:
            status = "open"
            print("Ticket criado e aguardando suporte disponível")

        result = self.ticket.create_ticket(
            id_client, id_support, id_ticket, status, defined_data, subject, description
        )
        return result
