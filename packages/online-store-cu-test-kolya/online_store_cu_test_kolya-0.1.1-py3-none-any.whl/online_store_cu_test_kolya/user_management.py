class UserManager:
    def __init__(self, users: dict = {}):
        self.users = users

    def add_user(self, user_id, user_data):
        if user_id in self.users.keys():
            print(f"Клиент с ID {user_id} уже существует")
        else:
            self.users[user_id] = user_data
            print(f'Клиент с ID {user_id} добавлен')

    def remove_user(self, user_id):
        if user_id in self.users.keys():
            del self.users[user_id]
            print(f'Клиент с ID {user_id} удалён')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def update_user(self, user_id, user_data):
        if user_id in self.users.keys():
            for k, v in user_data.items():
                self.users[user_id][k] = v
            print(f'Данные клиента с ID {user_id} обновлены')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def find_user(self, user_id):
        if user_id in self.users.keys():
            return self.users[user_id]
        else:
            print(f'Клиент с ID {user_id} не найден')
            return None
