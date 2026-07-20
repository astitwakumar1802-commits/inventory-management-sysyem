import sqlite3
import sys

def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            price REAL NOT NULL CHECK(price >= 0.0)
        )
    """)
    conn.commit()
    conn.close()

def add_item():
    print("\n--- Add New Item ---")
    name = input("Enter item name: ").strip().capitalize()
    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per unit: "))
        
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        conn.commit()
        print(f"✔️ Success: {name} added!")
    except sqlite3.IntegrityError:
        print("❌ Error: Item already exists.")
    except ValueError:
        print("❌ Error: Invalid input numbers.")
    finally:
        conn.close()

def view_inventory():
    print("\n--- Current Inventory ---")
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("Inventory is empty.")
        return

    print(f"{'Name':<20} | {'Quantity':<10} | {'Price ($)':<10}")
    print("-" * 48)
    for row in rows:
        print(f"{row[1]:<20} | {row[2]:<10} | ${row[3]:<10.2f}")

def update_by_name():
    print("\n--- Smart Update (By Product Name) ---")
    name = input("Enter the exact item name to update: ").strip().capitalize()
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name = ?", (name,))
    item = cursor.fetchone()
    
    if not item:
        print("❌ Error: Product not found!")
        conn.close()
        return
        
    print(f"Current Data -> Quantity: {item[2]}, Price: ${item[3]:.2f}")
    try:
        new_qty = int(input("Enter new quantity: "))
        new_price = float(input("Enter new price: "))
        
        cursor.execute("UPDATE items SET quantity = ?, price = ? WHERE name = ?", (new_qty, new_price, name))
        conn.commit()
        print(f"✔️ Success: {name} fields updated successfully!")
    except ValueError:
        print("❌ Error: Invalid numbers typed.")
    finally:
        conn.close()

def delete_by_name():
    print("\n--- Smart Delete (By Product Name) ---")
    name = input("Enter the item name to remove: ").strip().capitalize()
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE name = ?", (name, ))
    
    if cursor.rowcount == 0:
        print("❌ Error: No product found with that name.")
    else:
        conn.commit()
        print(f"⚠️ Success: {name} removed from the system.")
    conn.close()

def main():
    init_db()
    while True:
        print("\n=============================")
        print("    CUI INVENTORY CONSOLE")
        print("=============================")
        print("1. View Full Inventory")
        print("2. Add New Product")
        print("3. Update Product (By Name)")
        print("4. Remove Product (By Name)")
        print("5. Exit Console")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_by_name()
        elif choice == "4":
            delete_by_name()
        elif choice == "5":
            print("\nClosing console...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()