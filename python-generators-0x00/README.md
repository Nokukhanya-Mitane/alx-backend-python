# Python Generators – Database Seeder

## 🧩 Objective
Create a Python script that sets up a MySQL database `ALX_prodev`, creates a `user_data` table, and populates it from a CSV file (`user_data.txt`).

---

## 📚 Functions

| Function | Description |
|-----------|--------------|
| `connect_db()` | Connects to MySQL server |
| `create_database(connection)` | Creates database `ALX_prodev` if it doesn't exist |
| `connect_to_prodev()` | Connects to the `ALX_prodev` database |
| `create_table(connection)` | Creates `user_data` table |
| `insert_data(connection, data)` | Inserts CSV data into the table |

---

## ⚙️ Usage
```bash
chmod +x 0-main.py
./0-main.py
