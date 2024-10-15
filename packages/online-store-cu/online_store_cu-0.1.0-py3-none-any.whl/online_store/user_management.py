class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id: str, user_data: dict):
        if self.users.get(user_id):
            print(f"Клиент с ID {user_id} уже существует")
            return

        self.users[user_id] = user_data
        print(f"Клиент с ID {user_id} добавлен")

    def remove_user(self, user_id: str):
        if user_id not in self.users:
            print(f"Клиент с ID {user_id} не найден")
            return

        self.users.pop(user_id)
        print(f"Клиент с ID {user_id} удалён")

    def update_user(self, user_id: str, user_data: dict):
        if user_id not in self.users:
            print(f"Клиент с ID {user_id} не найден")
            return

        self.users[user_id] = user_data
        print(f"Данные клиента с ID {user_id} обновлены")

    def find_user(self, user_id: str) -> dict:
        if user_id not in self.users:
            print(f"Клиент с ID {user_id} не найден")
            return {}

        return self.users[user_id]
