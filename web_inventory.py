from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# --- HTML Template inside Python for single-file simplicity ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DVC Localhost Inventory</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #1e1e1e; color: white; padding: 30px; }
        h2 { color: #4CAF50; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border: 1px solid #444; text-align: left; }
        th { background-color: #333; }
        tr:nth-child(even) { background-color: #252525; }
        .form-group { margin-bottom: 15px; }
        input[type="text"], input[type="number"] { padding: 8px; width: 200px; margin-right: 10px; background:#333; color:white; border:1px solid #555; }
        button { padding: 8px 15px; background-color: #1f538d; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #2973c9; }
        .delete-btn { background-color: #c3073f; }
        .delete-btn:hover { background-color: #950740; }
    </style>
</head>
<body>
    <h2>🚀 DVC Inventory Management System (LOCALHOST MODE)</h2>
    
    <!-- ADD / UPDATE FORM -->
    <fieldset style="border: 1px solid #555; padding: 15px; border-radius: 5px;">
        <legend>Add / Update Product (By Name)</legend>
        <form action="/save" method="post">
            <input type="text" name="name" placeholder="Product Name" required>
            <input type="number" name="quantity" placeholder="Quantity" required>
            <input type="number" step="0.01" name="price" placeholder="Price" required>
            <button type="submit">Save Product</button>
        </form>
    </fieldset>

    <!-- INVENTORY TABLE -->
    <table>
        <tr>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Action</th>
        </tr>
        {% for row in items %}
        <tr>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>${{ "%.2f"|format(row[3]) }}</td>
            <td>
                <a href="/delete/{{ row[1] }}"><button class="delete-btn">Delete</button></a>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, items=items)

# यहाँ फिक्स किया है: methods=['POST'] कर दिया है
@app.route('/save', methods=['POST'])
def save_item():
    name = request.form['name'].strip().capitalize()
    qty = int(request.form['quantity'])
    price = float(request.form['price'])
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name=?", (name,))
    if cursor.fetchone():
        cursor.execute("UPDATE items SET quantity=?, price=? WHERE name=?", (qty, price, name))
    else:
        cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (name, qty, price))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<name>')
def delete_item(name):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE name=?", (name,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)