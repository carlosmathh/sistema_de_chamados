from queries.query_support import (
    SHOW_ALL_TICKETS_PROGRESS_SQL,
    SHOW_ALL_SUPPORT_TEAM_SQL,
    GET_SUPPORTS_AVAILABLE_SQL,
    GET_SUPPORT_SPECIFY,
    RESOLVED_CANCEL_TICKET_SQL,
    SHOW_ALL_TICKETS_PROGRESS_SQL,
    VALIDATE_TICKET_OWNER_SQL,
    REASSIGN_TICKET_SQL,
    GET_TICKET_COMFIRM_SQL,
    SHOW_TICKET_STATUS_SPECIFY_SQL,
    SHOW_TICKET_STATUS_ALL_SQL,
    GET_TICKETS_PROGRESS,
)
from src.mensages import Messages
from src.enum.ticket_result import Tickets_results


class SupportServices:
    def __init__(self, conn, utils, tickethistory) -> None:
        self.conn = conn
        self.utils = utils
        self.change_status_tickethistory = tickethistory

    # Funções Auxiliares -----------------------------------------------------
    # Pega todos os tickets ativos
    def get_all_active_tickets(self):
        with self.conn.cursor() as cursor:
            cursor.execute(SHOW_ALL_TICKETS_PROGRESS_SQL)
            datas = cursor.fetchall()
        return datas

    # Pega um supporte com tickets ativos
    def get_uni_support_active_tickets(self, id_support):
        with self.conn.cursor() as cursor:
            cursor.execute(GET_TICKETS_PROGRESS, (id_support))
            datas = cursor.fetchall()
            return datas

    # ALL SUPPORTS
    # MOSTRA TODOS OS SUPPORTERS
    def get_all_suporters(self):
        with self.conn.cursor() as cursor:
            cursor.execute(SHOW_ALL_SUPPORT_TEAM_SQL)
            datas = cursor.fetchall()
            self.utils.display_list(list(datas), "id", "name", "position_team")
            return datas

    # validar e capturar informações de um integrante da equipe
    def validate_support_id(self, tuple_all_support):
        id_ = self.utils.requests_id()
        return next(
            (
                (row["id"], row["position_team"])
                for row in tuple_all_support
                if row["id"] == id_
            ),
            None,
        )

    # PEGA E VALIDA SUPPORT PRONTO DISPONIVEl PARA TROCA
    def validate_support_eligible(self, id_, required_level):
        with self.conn.cursor() as cursor:
            cursor.execute(GET_SUPPORTS_AVAILABLE_SQL, (id_, required_level))
            tuple_supports = cursor.fetchall()
            if not tuple_supports:
                return Tickets_results.NO_AVAILABLE

            return tuple_supports

    # retorna dados com status especifico ou todos
    def get_tickets_open_resolved_cancel_all(self, choice_user):
        STATUS = {
            "1": "resolved",
            "2": "open",
            "3": "canceled",
            "4": ("in_progress", "resolved", "open", "canceled"),
        }
        choice = STATUS.get(choice_user)
        if not choice:
            return Messages.INVALID_OPTION

        try:
            with self.conn.cursor() as cursor:
                if choice_user in "123":
                    cursor.execute(SHOW_TICKET_STATUS_SPECIFY_SQL, (choice,))
                elif choice_user == "4":
                    cursor.execute(SHOW_TICKET_STATUS_ALL_SQL, choice)

                datas = cursor.fetchall()

            return list(datas)
        except Exception:
            return Tickets_results.ERROR

    # PEGA UM TICKET ESPECIFICO (ID, REQUIRED_LEVEL)
    def get_specify_ticket(self, id_ticket):
        with self.conn.cursor() as cursor:
            cursor.execute(GET_SUPPORT_SPECIFY, (id_ticket,))
            support = cursor.fetchone()
            current_support_id = support["id_support"] if support else None
            required_level = support["level"] if support else None
            return (current_support_id, required_level)

    def validate_ticket_owner(self, id_ticket, id_support):
        with self.conn.cursor() as cursor:
            cursor.execute(VALIDATE_TICKET_OWNER_SQL, (id_ticket, id_support))
            datas = cursor.fetchone()
            return datas

    # MUDA STATUS
    def change_status_ticket(
        self, id_support, id_ticket, status_choice, resolution_date
    ):
        tuple_tickets = self.get_uni_support_active_tickets(id_support)
        if not tuple_tickets:
            return Tickets_results.NO_ACTIVE_TICKETS

        id_valid = self.validate_ticket_owner(id_ticket, id_support)

        if id_valid is None:
            return Tickets_results.NOT_OWNER

        STATUS_MAP = {"1": "resolved", "2": "canceled"}
        status = STATUS_MAP.get(status_choice)

        if not status:
            return Tickets_results.INVALID_STATUS

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    RESOLVED_CANCEL_TICKET_SQL, (status, resolution_date, id_ticket)
                )

                self.change_status_tickethistory.log_event(
                    cursor,
                    id_ticket,
                    "status_changed",  # event_type
                    "support",  # actor_type
                    id_support,  # actor_id
                    "in_progress",  # old_value
                    f"new status: {status}",  # new_value
                    None,  # note
                )

                self.conn.commit()
            return Tickets_results.SUCCESS
        except Exception as e:
            self.conn.rollback()
            print(e)
            return Tickets_results.ERROR

    def get_ticket_to_comfirm(self, id_ticket):
        with self.conn.cursor() as cursor:
            cursor.execute(GET_TICKET_COMFIRM_SQL, id_ticket)
            comfitmation = cursor.fetchone()
            return comfitmation

    # TROCA TICKET DE SUPPOTER
    def reassign_support_ticket(self, id_user_action, id_ticket, id_new_owner):

        id_old_owner, required_level = self.get_specify_ticket(id_ticket)

        if not id_old_owner or not required_level:
            return Tickets_results.NOT_FOUND
        elif id_new_owner == id_old_owner:
            return Tickets_results.SAME_OWNER

        tuple_support_available = self.validate_support_eligible(
            id_new_owner, required_level
        )
        if not tuple_support_available:
            return Tickets_results.NO_AVAILABLE
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    REASSIGN_TICKET_SQL, (id_new_owner, id_ticket, id_new_owner)
                )
                if cursor.rowcount == 0:
                    self.conn.rollback()

                    comfitmation = self.get_ticket_to_comfirm(id_ticket)

                    if not comfitmation:
                        return Tickets_results.NOT_FOUND
                    print("no_support_available ")

                    return Tickets_results.NO_AVAILABLE

                self.change_status_tickethistory.log_event(
                    cursor,
                    id_ticket,
                    "reassigned",  # event_type
                    "support",  # actor_type
                    id_user_action,  # actor_id
                    f"id old_owner: {id_old_owner}",  # old_value
                    f"id new_owner: {id_new_owner}",  # new_value
                    None,  # note
                )

                self.conn.commit()
                return Tickets_results.SUCCESS

        except Exception as e:
            self.conn.rollback()
            self.expeption = e
            return Tickets_results.ERROR
