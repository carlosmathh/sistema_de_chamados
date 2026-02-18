class Session:

    def __init__(
        self,
    ) -> None:
        self.role = None
        self.id_user = None
        self.name = None
        self.position_team = None

    def keep_data(self, role, id_user, name, position_team):
        self.role = role
        self.id_user = id_user
        self.name = name
        self.position_team = position_team

    def logout(self):
        self.role = self.id_user = self.name = self.position_team = None

    def is_active(self):
        return self.id_user is not None
