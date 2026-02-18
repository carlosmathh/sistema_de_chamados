from queries.query_menu import GET_DATA_CLIENT_SQL, GET_DATA_SUPPORT_SQL
from db.connection import get_connection


class AuthService:
    def __init__(self) -> None:
        self.conn = get_connection()

    def get_data_by_id(self, table, id_):
        option = {
            "1": {"sql": GET_DATA_CLIENT_SQL, "role": "client"},
            "2": {"sql": GET_DATA_SUPPORT_SQL, "role": "support"},
        }
        config = option.get(str(table))
        if not config:
            return None

        sql = config["sql"]
        role = config["role"]

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_,))
                datas = cursor.fetchone()
                if not datas:
                    return None

                id_user = datas.get("id")
                name_user = datas.get("name")
                position_team = datas.get("position_team")

                return (role, id_user, name_user, position_team)
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return None
