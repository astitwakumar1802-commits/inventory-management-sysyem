import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GUI Inventory Dashboard")
        self.state('zoomed')
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # LEFT PANEL
        left_panel = ctk.CTkFrame(self, width=280, corner_radius=10)
        left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        left_panel.grid_propagate(False)

        ctk.CTkLabel(left_panel, text="Product Control", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        # Entry Boxes
        self.entry_name = ctk.CTkEntry(left_panel, placeholder_text="Item Name (Required)", width=220)
        self.entry_name.pack(pady=10)

        self.entry_qty = ctk.CTkEntry(left_panel, placeholder_text="New/Current Quantity", width=220)
        self.entry_qty.pack(pady=10)

        self.entry_price = ctk.CTkEntry(left_panel, placeholder_text="New/Current Price", width=220)
        self.entry_price.pack(pady=10)

        # Operational Buttons
        ctk.CTkButton(left_panel, text="➕ Add Product", command=self.add_item, width=220).pack(pady=10)
        ctk.CTkButton(left_panel, text="🔄 Update (By Name)", command=self.update_by_name, width=220, fg_color="#2b7a78", hover_color="#174d4c").pack(pady=10)
        ctk.CTkButton(left_panel, text="🗑️ Delete (By Name)", command=self.delete_by_name, width=220, fg_color="#c3073f", hover_color="#950740").pack(pady=10)
        ctk.CTkButton(left_panel, text="🧹 Clear Fields", command=self.clear_entries, width=220, fg_color="transparent", border_width=1).pack(pady=10)

        # RIGHT PANEL (TABLE)
        right_panel = ctk.CTkFrame(self, corner_radius=10)
        right_panel.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", fieldbackground="#2b2b2b", foreground="white", rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background="#1f1f1f", foreground="white", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        columns = ("name", "qty", "price")
        self.tree = ttk.Treeview(right_panel, columns=columns, show="headings")
        
        self.tree.heading("name", text="Product Name")
        self.tree.heading("qty", text="Quantity in Stock")
        self.tree.heading("price", text="Price ($)")

        self.tree.column("name", width=250, anchor="w")
        self.tree.column("qty", width=120, anchor="center")
        self.tree.column("price", width=120, anchor="center")
        
        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, price FROM items")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(row[0], row[1], f"${row[2]:.2f}"))
        conn.close()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.clear_entries()
        self.entry_name.insert(0, values[0])
        self.entry_qty.insert(0, values[1])
        self.entry_price.insert(0, values[2].replace('$', ''))

    def add_item(self):
        name = self.entry_name.get().strip().capitalize()
        if not name:
            messagebox.showerror("Error", "Product Name is required!")
            return
        try:
            qty = int(self.entry_qty.get())
            price = float(self.entry_price.get())
            
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (name, qty, price))
            conn.commit()
            conn.close()
            self.refresh_table()
            self.clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Product already exists!")
        except ValueError:
            messagebox.showerror("Error", "Fill Quantity and Price with valid numbers.")

    def update_by_name(self):
        name = self.entry_name.get().strip().capitalize()
        if not name:
            messagebox.showerror("Error", "Enter Product Name to update.")
            return
        try:
            new_qty = int(self.entry_qty.get())
            new_price = float(self.entry_price.get())
            
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET quantity = ?, price = ? WHERE name = ?", (new_qty, new_price, name))
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No product found with this name!")
            else:
                conn.commit()
                messagebox.showinfo("Success", f"{name} database records updated!")
            conn.close()
            self.refresh_table()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please input valid numbers for quantity & price.")

    def delete_by_name(self):
        name = self.entry_name.get().strip().capitalize()
        if not name:
            return
        if messagebox.askyesno("Confirm", f"Delete {name} permanently?"):
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE name = ?", (name,))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Product not found.")
            else:
                conn.commit()
            conn.close()
            self.refresh_table()
            self.clear_entries()

    def clear_entries(self):
        self.entry_name.delete(0, 'end')
        self.entry_qty.delete(0, 'end')
        self.entry_price.delete(0, 'end')

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()