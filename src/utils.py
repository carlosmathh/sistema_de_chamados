from datetime import datetime
from src.mensages import Messages


class Utils:

    # VALIDAÇÕES
    def valid_int(self, value):
        try:
            if int(value) <= 0:
                return None
            return int(value)
        except ValueError:
            return None

    def valid_id(self, id_: int | None, list_id: list):
        if id_ in list_id:
            return id_
        return None

    # solicita dados
    def requests_id(self):
        id_ = input(Messages.WRITE_ID)

        value = self.valid_int(id_)
        if not value:
            return None
        return value

    # veriica se o id existe na lista
    def get_ids_in_list(self, datas: list):
        if not datas:
            return []
        return [row["id"] for row in datas if "id" in row]

    # define data de agora
    def define_date_now(self):
        now = datetime.now()
        date_now = now.strftime("%Y-%m-%d %H:%M:%S")
        return date_now

    # EXIBIR_listas
    def display_list(self, data_list: list | tuple, *columns):
        if not data_list:
            print("\n" + "=" * 30)
            print(Messages.MESSAGE_NOT_TICKET_PROGRESS)
            print("=" * 30 + "\n")
            return  # Sai da função se estiver vazio

        width = 20
        # O cabeçalho e o loop devem estar aqui dentro!
        header = " | ".join([f"{col.upper():<{width}}" for col in columns])
        print("\n" + header)
        print("-" * len(header))

        for row in data_list:
            # Usamos row.get(col) ou row[col] dependendo de como o cursor retorna (dict ou tuple)
            # O str(row[col] or "N/A") trata os valores NULL/None que conversamos
            line = " | ".join(
                [f"{str(row.get(col) or 'N/A'):<{width}}" for col in columns]
            )
            print(line)
        print("\n")
