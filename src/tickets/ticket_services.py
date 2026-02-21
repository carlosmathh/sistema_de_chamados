from queries.query_ticket import UPDATE_TICKET_STATUS, GET_TICKET_OWNER_SUPPORT
from queries.query_ticket import GET_TICKET_DETAILS
from queries.query_ticket import (
    GET_MY_TICKETS_CLIENT,
    GET_MY_TICKETS_CLIENT_STATUS,
    GET_MY_TICKETS_SUPPORT,
    GET_MY_TICKETS_SUPPORT_STATUS,
)
from queries.query_audit import LIST_TICKET_HISTORY_SQL
from queries.query_problem_category import LIST_PROBLEM_CATEGORIES_SQL
from queries.query_support import (
    SHOW_TICKET_STATUS_SPECIFY_SQL,
    SHOW_TICKET_STATUS_ALL_SQL,
    SHOW_TICKET_STATUS_SPECIFY_FRONT_SQL,
    SHOW_TICKET_STATUS_ALL_FRONT_SQL,
)
from queries.query_support import (
    LIST_AVAILABLE_SUPPORTS_FRONT_SQL,
    REASSIGN_TICKET_FRONT_SQL,
)
from src.audit.ticket_history_service import TicketHistoryService

from queries.queries import Queries
from datetime import datetime

from src.assign_support import AssingSupport
from src.utils import Utils
import pymysql


class TicketServices:
    def __init__(self, conn):
        self.conn = conn

    def get_ticket_details(self, ticket_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(GET_TICKET_DETAILS, (ticket_id,))
            return cursor.fetchone()

    def get_ticket_support_owner(self, ticket_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute(GET_TICKET_OWNER_SUPPORT, (ticket_id,))
            return cursor.fetchone()

    def update_ticket_status(self, ticket_id: int, new_status: str):
        with self.conn.cursor() as cursor:
            cursor.execute(UPDATE_TICKET_STATUS, (new_status, new_status, ticket_id))
        self.conn.commit()

    def update_ticket_status_and_return(
        self,
        ticket_id: int,
        new_status: str,
        actor_type: str,
        actor_id: int,
    ):
        history = TicketHistoryService()

        with self.conn.cursor() as cursor:
            # 1) pegar status antigo
            cursor.execute(GET_TICKET_DETAILS, (ticket_id,))
            row = cursor.fetchone()

            if not row:
                return None

            old_status = row["status"] if isinstance(row, dict) else row[1]

            # 2) atualizar status
            cursor.execute(UPDATE_TICKET_STATUS, (new_status, new_status, ticket_id))

            # 3) registrar histórico
            history.log_event(
                cursor=cursor,
                id_ticket=ticket_id,
                event_type="status_changed",
                old_value=old_status,
                new_value=new_status,
                actor_type=actor_type,
                actor_id=actor_id,
                note=None,
            )

        # commit único
        self.conn.commit()

        # 4) retornar ticket atualizado
        return self.get_ticket_details(ticket_id)

    def get_my_tickets(self, user_role: str, user_id: int, status: str | None = None):
        if user_role == "client":
            if status:
                sql = GET_MY_TICKETS_CLIENT_STATUS
                params = (user_id, status)
            else:
                sql = GET_MY_TICKETS_CLIENT
                params = (user_id,)
        elif user_role == "support":
            if status:
                sql = GET_MY_TICKETS_SUPPORT_STATUS
                params = (user_id, status)
            else:
                sql = GET_MY_TICKETS_SUPPORT
                params = (user_id,)
        else:
            return []

        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

    def get_problem_categories(self):
        with self.conn.cursor() as cursor:
            cursor.execute(LIST_PROBLEM_CATEGORIES_SQL)
            return cursor.fetchall()

    def create_ticket(
        self,
        client_id: int,
        problem_category_id: int,
        subject: str | None,
        description: str | None,
    ):
        utils = Utils()
        assigner = AssingSupport(self.conn, utils)

        support_id = assigner.assign_support(problem_category_id)
        status = "in_progress" if support_id else "open"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.conn.cursor() as cursor:
            cursor.execute(
                Queries.CREATE_TICKET_FRONT_SQL,
                (
                    client_id,
                    support_id,
                    problem_category_id,
                    status,
                    now,
                    subject,
                    description,  # ← nome correto
                ),
            )
            ticket_id = cursor.lastrowid

        self.conn.commit()
        return ticket_id

    def get_ticket_history(self, ticket_id: int):
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(LIST_TICKET_HISTORY_SQL, (ticket_id,))
            return cursor.fetchall()

    def get_tickets_by_status(self, status: str | None):
        with self.conn.cursor() as cursor:
            if status and status != "all":
                cursor.execute(SHOW_TICKET_STATUS_SPECIFY_SQL, (status,))
                return cursor.fetchall()

            # all
            cursor.execute(
                SHOW_TICKET_STATUS_ALL_SQL,
                ("in_progress", "resolved", "open", "canceled"),
            )
            return cursor.fetchall()

    def list_all_tickets_by_status(self, status: str):
        with self.conn.cursor() as cursor:
            if status == "all":
                cursor.execute(
                    SHOW_TICKET_STATUS_ALL_FRONT_SQL,
                    ("in_progress", "resolved", "open", "canceled"),
                )
                return cursor.fetchall()

            cursor.execute(SHOW_TICKET_STATUS_SPECIFY_FRONT_SQL, (status,))
            return cursor.fetchall()

    def list_board_tickets(self, status: str):
        with self.conn.cursor() as cursor:
            if status == "all":
                cursor.execute(
                    SHOW_TICKET_STATUS_ALL_SQL,
                    ("open", "in_progress", "resolved", "canceled"),
                )
                return cursor.fetchall()

            cursor.execute(SHOW_TICKET_STATUS_SPECIFY_SQL, (status,))
            return cursor.fetchall()

    def list_available_supports_for_ticket(self, ticket_id: int):
        details = self.get_ticket_details(ticket_id)
        if not details:
            return None, "Ticket not found"

        # só reatribui ticket em andamento
        status = details["status"] if isinstance(details, dict) else details[1]
        if status != "in_progress":
            return [], "Only in_progress tickets can be reassigned"

        with self.conn.cursor() as cursor:
            cursor.execute(LIST_AVAILABLE_SUPPORTS_FRONT_SQL, (ticket_id,))
            return cursor.fetchall(), None

    def reassign_ticket_and_return(
        self, ticket_id: int, new_support_id: int, actor_type: str, actor_id: int
    ):
        history = TicketHistoryService()

        details = self.get_ticket_details(ticket_id)
        if not details:
            return None, "Ticket not found"

        status = details["status"] if isinstance(details, dict) else details[1]
        if status != "in_progress":
            return None, "Only in_progress tickets can be reassigned"

        required_level = (
            details["required_level"] if isinstance(details, dict) else details[8]
        )
        old_support_id = (
            details["support_id"] if isinstance(details, dict) else details[9]
        )

        # valida se new_support é elegível pelas mesmas regras (active, level >= required, <3 tickets)
        with self.conn.cursor() as cursor:
            cursor.execute(LIST_AVAILABLE_SUPPORTS_FRONT_SQL, (ticket_id,))
            candidates = cursor.fetchall() or []

            # pega ids
            candidate_ids = set()
            for c in candidates:
                cid = c["id"] if isinstance(c, dict) else c[0]
                candidate_ids.add(cid)

            if new_support_id not in candidate_ids:
                return None, "Selected support is not available for this ticket"

            # faz update (evita mesmo owner e só se in_progress)
            cursor.execute(
                REASSIGN_TICKET_FRONT_SQL,
                (new_support_id, new_support_id, ticket_id, new_support_id),
            )
            if cursor.rowcount == 0:
                return (
                    None,
                    "Reassignment not applied (same owner, not in_progress, or insufficient level)",
                )

            # log de auditoria
            history.log_event(
                cursor=cursor,
                id_ticket=ticket_id,
                event_type="reassigned",
                old_value=str(old_support_id) if old_support_id is not None else None,
                new_value=str(new_support_id),
                actor_type=actor_type,
                actor_id=actor_id,
                note="manual reassignment",
            )

        self.conn.commit()
        return self.get_ticket_details(ticket_id), None
