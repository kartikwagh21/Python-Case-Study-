import datetime

class AlertSystem:
    @staticmethod
    def stock_alert_decorator(func):
        """Decorator to check stock levels after any transaction."""
        def wrapper(self, item_name, amount):
            result = func(self, item_name, amount)
            item = self.inventory.get(item_name)
            if item and item.quantity <= item.reorder_point:
                AlertSystem.generate_alert(item)
            return result
        return wrapper

    @staticmethod
    def generate_alert(item):
        alert_msg = f"[ALERT] {datetime.datetime.now()} - {item.name} is low! (Current: {item.quantity})"
        print(alert_msg)
        with open("reorder_list.txt", "a") as f:
            f.write(alert_msg + "\n")