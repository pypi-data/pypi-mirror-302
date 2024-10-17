

class OrderManager:
    def __init__(self, orders: dict = {}):
        self.orders = orders

    def create_order(self, order_id, order_data):
        if order_id in self.orders.keys():
            print(f"Заказ с ID {order_id} уже существует")
        else:
            self.orders[order_id] = order_data
            print(f"Заказ с ID {order_id} создан")

    def update_order(self, order_id, order_data):
        if order_id not in self.orders.keys():
            print(f"Заказ с ID {order_id} не найден")
        else:
            for k, v in order_data.items():
                self.orders[order_id][k] = v
            print(f'Заказ с ID {order_id} обновлён')

    def cancel_order(self, order_id):
        if order_id not in self.orders.keys():
            print(f'Заказ с ID {order_id} не найден')
        else:
            del self.orders[order_id]
            print(f'Заказ с ID {order_id} отменён')