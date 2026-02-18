from queries.query_search import (
    SEARCH_BY_ID_CLIENT,
    SEARCH_BY_ID_CLIENT_STATUS,
    SEARCH_BY_ID_SUPPORT,
    SEARCH_BY_ID_SUPPORT_STATUS,
    SEARCH_FOR_TEXT_CLIENT,
    SEARCH_FOR_TEXT_CLIENT_STATUS,
    SEARCH_FOR_TEXT_SUPPORT,
    SEARCH_FOR_TEXT_SUPPORT_STATUS,
)

from src.mensages import Messages


class SearchServices:
    def __init__(self, conn) -> None:
        self.conn = conn

    def search_ticket_by_id(self, user_role, ticket_id, client_id=None, status=None):
        if user_role == "client":
            if status == None:
                sql = SEARCH_BY_ID_CLIENT
                params = (ticket_id, client_id)
            else:
                sql = SEARCH_BY_ID_CLIENT_STATUS
                params = (ticket_id, client_id, status)

        elif user_role == "support":
            if status == None:
                sql = SEARCH_BY_ID_SUPPORT
                params = (ticket_id,)
            else:
                sql = SEARCH_BY_ID_SUPPORT_STATUS
                params = (ticket_id, status)
        else:
            return None

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)

                data_search = cursor.fetchone()
                return data_search

        except Exception as e:
            return f"{Messages.ERROR}, {e}"

    def search_tickets_by_text(self, user_role, text, client_id=None, status=None):
        like = f"%{text.strip()}%"

        if user_role == "client":
            if status is None:
                sql = SEARCH_FOR_TEXT_CLIENT
                params = (client_id, like, like)
            else:

                sql = SEARCH_FOR_TEXT_CLIENT_STATUS
                params = (client_id, like, like, status)

        elif user_role == "support":
            if status is None:
                sql = SEARCH_FOR_TEXT_SUPPORT
                params = (like, like)
                print(f"DEBUG SQL: {sql}")
                print(f"DEBUG PARAMS: {params}")
            else:
                sql = SEARCH_FOR_TEXT_SUPPORT_STATUS
                params = (like, like, status)
                print(f"DEBUG SQL: {sql}")
                print(f"DEBUG PARAMS: {params}")
        else:
            return None

        try:
            with self.conn.cursor() as cursor:

                cursor.execute(sql, params)

                data_search = cursor.fetchall()
                return data_search

        except Exception as e:
            return f"{Messages.ERROR}, {e}"
