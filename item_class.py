class Item:
    def __init__(self, name, quantity, reorder_point):
        self.name = name
        self.quantity = int(quantity)
        self.reorder_point = int(reorder_point)

    def __str__(self):
        return f"{self.name}: Qty {self.quantity} (Threshold: {self.reorder_point})"