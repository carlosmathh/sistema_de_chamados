# type: ignore
from queries.query_problem_category import LIST_PROBLEM_CATEGORIES_SQL
from src.mensages import Messages


class Problem_categories:
    def __init__(self, conn, utils) -> None:
        self.conn = conn
        self.utils = utils

    def display_problem_categories(self):
        with conn.cursor() as cursor:
            cursor.execute(LIST_PROBLEM_CATEGORIES_SQL)
            datas = cursor.fetchall()
            self.utils.display_list(datas, "id", "name", "descript", "base_complexity")
            print(Messages.MENSAGE_COD_101)
            self.list_id_ticket = self.utils.get_ids_in_list(datas)

    def id_in_problem_categories(self):
        id_ = self.utils.requests_id()
        id_valid_ticket = self.utils.valid_id(id_, self.list_id_ticket)
        return id_, id_valid_ticket
