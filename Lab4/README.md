# 🏭 Warehouse Inventory Viewer

A simple HTTP server written in Python that aggregates and displays warehouse inventory data based on the selected warehouses in the URL.

## 🚀 Features

- Serve inventory data from multiple warehouse files.
- Combine inventory across selected warehouses.
- Clean HTML output displaying product quantities.
- Dynamic URL selection (e.g., `/1`, `/2_3_5`).
- Displays warehouse names for clarity.

## 📁 Project Structure

```
project/
│
├── data/
│   ├── warehouse1.txt
│   ├── warehouse2.txt
│   ├── warehouse3.txt
│   ├── warehouse4.txt
│   └── warehouse5.txt
│
├── server.py
└── README.md
```

Each `warehouseX.txt` file contains product data in the format:
```
ProductName: Quantity
```

Example:
```
Health Potion: 10
Mana Crystal: 5
```

## 🖥️ How to Run

1. Make sure Python 3 is installed.
2. Place the data files inside the `data/` directory.
3. Run the server:

```bash
python server.py
```

4. Open your browser and navigate to:

- `http://localhost:8080/` – to see the instructions
- `http://localhost:8080/1_3` – to view inventory from Iron Keep and Echo Bay Depot

## 🧪 Example URLs

- `http://localhost:8080/1` → View inventory from Iron Keep
- `http://localhost:8080/2_4` → View combined inventory from Crystal Vault and Solaris Hub
- `http://localhost:8080/1_2_3_4_5` → View all warehouses

## ⚠️ Notes

- Missing or invalid warehouse IDs are ignored.
- If no data is found, an appropriate message is shown.
