class OrderManager:
    def __init__(self):
        self.orders = {}

    def create_order(self, order_id: str, order_data: dict):
        if order_id in self.orders:
            print(f"Заказ с ID {order_id} уже существует")
            return

        self.orders[order_id] = order_data
        print(f"Заказ с ID {order_id} добавлен")

    def update_order(self, order_id: str, order_data: dict):
        if order_id not in self.orders:
            print(f"Заказ с ID {order_id} не найден")
            return

        self.orders[order_id] = order_data
        print(f"Заказ с ID {order_id} обновлён")

    def cancel_order(self, order_id: str):
        if order_id not in self.orders:
            print(f"Заказ с ID {order_id} не найден")
            return

        self.orders.pop(order_id)
        print(f"Заказ с ID {order_id} отменён")
