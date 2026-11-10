# object relational mapping (ORM)
# is a programming technique for converting data between incompatible 
# type systems in object-oriented programming languages. This creates, in effect, a "virtual object database" 
# that can be used from within the programming language.

class inventory:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS inventory (
            id SERIAL PRIMARY KEY,
            name VARCHAR(250) NOT NULL,
            qty INTEGER NOT NULL,
            buying_price INTEGER NOT NULL,
            selling_price INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            cursor.execute(
                "ALTER TABLE inventory "
                "ADD COLUMN IF NOT EXISTS qty INTEGER NOT NULL DEFAULT 0"
            )
            print("Inventory table created successfully.")

    def add_item(self, name, qty, buying_price, selling_price):
        query = """
        INSERT INTO inventory (name, qty, buying_price, selling_price)
        VALUES (%s, %s, %s, %s)
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(query, (name, qty, buying_price, selling_price))
            print(f"Item '{name}' added to inventory.")

    def get_all_items(self):
        query = "SELECT * FROM inventory"
        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


if __name__ == "__main__":
    from db import Database

    db = Database()
    inventory = inventory(db)
    inventory.create_table()
    inventory.add_item("item1", 10, 100, 150)
    items = inventory.get_all_items()
    print(items)