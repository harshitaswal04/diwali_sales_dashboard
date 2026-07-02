# 🪔 Diwali Sales Dashboard

A Python + MySQL project for managing, analyzing, and visualizing Diwali sales data. The project provides a full CRUD console application backed by MySQL, along with Seaborn-powered chart visualizations for sales insights.

## 📁 Project Files

- [`sql.py`](./sql.py) — Main Python application: database table management, CRUD operations, CSV export, and chart visualization
- [`diwalisales.sql`](./diwalisales.sql) — SQL dump for the `diwali sales data` table

## 🚀 Features

- **Table Structure Management** — Creates the `diwali sales data` table (with an added `row_id` primary key for safe CRUD operations)
- **CRUD Operations** — Add, update, delete, and view sales transactions
- **CSV Export** — Export all sales records to a CSV file
- **Data Visualization** — Generate Seaborn charts directly from the MySQL database:
  - Total Amount by State
  - Total Orders by Product Category
  - Age Distribution
  - Total Amount by Zone per Gender

## 🛠️ Tech Stack

- Python (`mysql-connector-python`, `pandas`, `matplotlib`, `seaborn`)
- MySQL

## 📊 Dashboard Visualizations

### Total Amount by State
![Total Amount by State](./images/chart_amount_by_state.png)

### Total Orders by Product Category
![Total Orders by Product Category](./images/chart_orders_by_category.png)

### Age Distribution
![Age Distribution](./images/chart_age_distribution.png)

### Total Amount by Zone per Gender
![Total Amount by Zone per Gender](./images/chart_amount_by_zone_gender.png)

## ⚙️ Setup & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/diwali_sales_dashboard.git
   cd diwali_sales_dashboard
   ```

2. Install dependencies:
   ```bash
   pip install mysql-connector-python pandas matplotlib seaborn
   ```

3. Set up the MySQL database using the provided schema:
   ```bash
   mysql -u root -p < diwalisales.sql
   ```

4. Update the `DB_CONFIG` dictionary in `sql.py` with your own MySQL credentials.

5. Run the application:
   ```bash
   python sql.py
   ```

6. Use the interactive console menu to add/update/delete records, export data, or generate charts.

## 🖥️ Console Menu

```
============= DIWALI SALES DATABASE CONTROL PANEL =============
1. Add New Sale Record
2. Update Sale Amount
3. Delete Sale Record
4. View All Sales (SELECT *)
5. Export Database Rows to CSV File
6. Generate Chart Visualisation (Seaborn)
7. Exit Terminal Application
==================================================================
```

## 📂 Repository Structure

```
diwali_sales_dashboard/
├── sql.py
├── diwalisales.sql
├── images/
│   ├── chart_amount_by_state.png
│   ├── chart_orders_by_category.png
│   ├── chart_age_distribution.png
│   └── chart_amount_by_zone_gender.png
└── README.md
```

## 📜 License

This project is open source and available under the MIT License.

---

## 👤 Author

**HARSHIT_ASWAL**
📧 mailto://harshitaswal04@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/harshit-aswal) | [GitHub](https://github.com/harshitaswal04)

Feel free to open an issue or reach out if you have questions or suggestions!

---

⭐ **If you found this project helpful, please give it a star!**
