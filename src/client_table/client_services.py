from queries.query_ticket import INSERT_TICKET_SQL
from queries.query_client import DISPLAY_TICKETS_CLIENT_SQL
from src.audit.ticket_history_service import TicketHistoryService
from src.enum.ticket_result import Tickets_results


class ClientServices:
    def __init__(self, conn) -> None:
        self.history = TicketHistoryService()
        self.conn = conn

    def get_ticket_by_client(self, id_client):
        with self.conn.cursor() as cursor:
            cursor.execute(DISPLAY_TICKETS_CLIENT_SQL, (id_client,))
            data = cursor.fetchall()
            return data

    def create_ticket(
        self,
        id_client,
        id_support,
        id_problem_category,
        status,
        defined_data,
        subject,
        description,
    ):
        list_insert = (
            id_client,
            id_support,
            id_problem_category,
            status,
            defined_data,
            subject,
            description,
        )
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(INSERT_TICKET_SQL, list_insert)
                id_ticket_create = cursor.lastrowid

                self.history.log_event(
                    cursor,
                    id_ticket_create,
                    "created",  # event_type
                    "client",  # actor_type
                    id_client,  # actor_id
                    None,  # old_value
                    None,  # new_value
                    note=f"Subject: {subject}",  # note
                )

                if id_support:
                    self.history.log_event(
                        cursor,
                        id_ticket_create,
                        "assigned",  # event_type
                        "system",  # actor_type
                        None,  # actor_id
                        None,  # old_value
                        f"new_owner: {str(id_support)}",  # new_value
                        "assigned automatically",  # note
                    )

                self.conn.commit()
                return Tickets_results.SUCCESS
        except Exception:
            self.conn.rollback()

            return Tickets_results.ERROR
