from src.mensages import Messages
from src.support.support_services import SupportServices


class SupportFlow:
    def __init__(self, conn, utils, tickethistory) -> None:
        self.conn = conn
        self.utils = utils
        self.tickethistory = tickethistory
        self.services = SupportServices(self.conn, self.utils, self.tickethistory)

    def change_status(self, id_support):
        id_ticket = self.utils.requests_id()
        status_choice = input(Messages.INPUT_CHANGE_STATUS)
        resolution_date = self.utils.define_date_now()

        return self.services.change_status_ticket(
            id_support, id_ticket, status_choice, resolution_date
        )

    def reassign_ticket(self, id_user_action):
        id_ticket = self.utils.requests_id()
        print(Messages.INPUT_ID_SUPPORT)
        id_new_owner = self.utils.requests_id()

        return self.services.reassign_support_ticket(
            id_user_action, id_ticket, id_new_owner
        )

    def get_user_choice_open_resolved_cancel(self):
        choice_user = input(Messages.INPUT_CHOICE_STATUS)
        datas = self.services.get_tickets_open_resolved_cancel_all(choice_user)

        return datas
