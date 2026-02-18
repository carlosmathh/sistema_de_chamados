from queries.query_problem_category import SHOW_PROBLEM_CATE_SPECIFY_SQL
from queries.query_support import SHOW_POSITION_TEAM_SQL


class AssingSupport:
    def __init__(self, conn, utils) -> None:
        self.conn = conn
        self.utils = utils

    def search_required_level(self, id_problem_categories: int):

        with self.conn.cursor() as cursor:
            cursor.execute(SHOW_PROBLEM_CATE_SPECIFY_SQL, (id_problem_categories,))
            required_level_dict = cursor.fetchone()

            if not required_level_dict:
                return None

            return required_level_dict

    def search_position_team(self, required_dict: dict):
        required_level = required_dict["required_level"]

        with self.conn.cursor() as cursor:
            cursor.execute(SHOW_POSITION_TEAM_SQL, (required_level,))
            position_team = cursor.fetchall()

            if not position_team:
                return None

            return position_team

    def assign_support(self, id_problem_categories):
        required_level_dict = self.search_required_level(id_problem_categories)

        if not required_level_dict:
            return None

        lucky_support = self.search_position_team(required_level_dict)

        if not lucky_support:
            return None

        return lucky_support[0]["id"]
