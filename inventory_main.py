import csv
import matplotlib.pyplot as plt
from item_class import Item
from alert_system import AlertSystem

class StockManager:
    def __init__(self, file_path="inventory.csv"):
        self.file_path = file_path
        self.inventory = {}
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.inventory[row['name']] = Item(row['name'], row['quantity'], row['reorder_point'])
        except FileNotFoundError:
            print("No inventory file found. Starting fresh.")

    def save_to_file(self):
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "quantity", "reorder_point"])
            writer.writeheader()
            for item in self.inventory.values():
                writer.writerow({'name': item.name, 'quantity': item.quantity, 'reorder_point': item.reorder_point})

    def add_new_stock(self, name, qty, threshold):
        self.inventory[name] = Item(name, qty, threshold)
        self.save_to_file()

    @AlertSystem.stock_alert_decorator
    def record_sale(self, name, amount):
        if name in self.inventory:
            if self.inventory[name].quantity >= amount:
                self.inventory[name].quantity -= amount
                self.save_to_file()
                return True
        return False

    def get_low_stock_items(self):
        # Using Lambda to filter low stock items
        low_stock = list(filter(lambda x: x.quantity <= x.reorder_point, self.inventory.values()))
        return low_stock

    def visualize_inventory(self):
        names = list(self.inventory.keys())
        quantities = [item.quantity for item in self.inventory.values()]
        thresholds = [item.reorder_point for item in self.inventory.values()]

        plt.figure(figsize=(10, 6))
        plt.bar(names, quantities, color='skyblue', label='Current Stock')
        plt.step(names, thresholds, where='mid', color='red', label='Reorder Point', linestyle='--')
        plt.xlabel('Product Name')
        plt.ylabel('Quantity')
        plt.title('Grocery Inventory Levels')
        plt.legend()
        plt.show()

# --- Execution Example ---
if __name__ == "__main__":
    manager = StockManager()
    
    # Adding initial items if csv is empty
    if not manager.inventory:
        manager.add_new_stock("Milk", 50, 10)
        manager.add_new_stock("Bread", 20, 5)
        manager.add_new_stock("Eggs", 100, 20)

    print("Current Inventory Loaded.")
    
    # Simulating a sale that triggers an alert
    print("\nSelling 16 loaves of Bread...")
    manager.record_sale("Bread", 16) 
    
    # Data Analysis
    low_items = manager.get_low_stock_items()
    print(f"\nItems needing reorder: {[i.name for i in low_items]}")
    
    # Data Visualization
    manager.visualize_inventory()