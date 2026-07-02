import csv
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # safe backend for non-interactive/terminal use
import matplotlib.pyplot as plt
import seaborn as sns

# Define connection parameters globally for convenience
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'H@rshit1234',
    'database': 'coffee_shop_sales_db'
}

def get_connection():
    """Establishes and returns a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# =====================================================================
# 1. TABLE STRUCTURE MANAGEMENT (DDL)
# =====================================================================

def manage_table_structure():
    """Demonstrates how to create, alter, and drop a table safely."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # A. CREATE TABLE (Creates your specified coffee_shop_sales table)
        create_query = """
        CREATE TABLE IF NOT EXISTS coffee_shop_sales (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_date DATE,
            transaction_time TIME,
            transaction_qty INT,
            store_id INT,
            store_location TEXT,
            product_id INT,
            unit_price DOUBLE,
            product_category TEXT,
            product_type TEXT,
            product_detail TEXT
        )
        """
        cursor.execute(create_query)
        print("Table 'coffee_shop_sales' verified/created successfully.")

        # B. ALTER TABLE (Example: Safely adding a temporary column)
        cursor.execute("ALTER TABLE coffee_shop_sales ADD COLUMN temp_notes TEXT")
        print("Table altered: Added 'temp_notes' column.")

        # C. DROP COLUMN (Example: Dropping the temporary column to keep things clean)
        cursor.execute("ALTER TABLE coffee_shop_sales DROP COLUMN temp_notes")
        print("Table altered: Dropped 'temp_notes' column.")

        connection.commit()
    except Error as e:
        print(f"Structure Management Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# 2. DATA MANIPULATION OPERATIONS (CRUD)
# =====================================================================

def insert_sale(date, time, qty, store_id, loc, prod_id, price, cat, p_type, detail):
    """Inserts a new record using parameterized queries to prevent SQL injection."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO coffee_shop_sales 
        (transaction_date, transaction_time, transaction_qty, store_id, store_location, 
         product_id, unit_price, product_category, product_type, product_detail)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (date, time, qty, store_id, loc, prod_id, price, cat, p_type, detail)
        
        cursor.execute(query, data)
        connection.commit()
        print(f"\n[SUCCESS] Data added! Inserted Transaction ID: {cursor.lastrowid}")
    except Error as e:
        print(f"\n[ERROR] Insert Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_sale_quantity(transaction_id, new_qty):
    """Updates the transaction quantity for a specific transaction ID."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = "UPDATE coffee_shop_sales SET transaction_qty = %s WHERE transaction_id = %s"
        cursor.execute(query, (new_qty, transaction_id))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"\n[SUCCESS] Data updated! Affected rows: {cursor.rowcount}")
        else:
            print(f"\n[WARNING] No record found with Transaction ID: {transaction_id}")
    except Error as e:
        print(f"\n[ERROR] Update Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_sale(transaction_id):
    """Deletes a record based on its transaction ID."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = "DELETE FROM coffee_shop_sales WHERE transaction_id = %s"
        cursor.execute(query, (transaction_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"\n[SUCCESS] Data deleted! Affected rows: {cursor.rowcount}")
        else:
            print(f"\n[WARNING] No record found with Transaction ID: {transaction_id}")
    except Error as e:
        print(f"\n[ERROR] Delete Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# 3. EXPORT DATA TO CSV & DISPLAY ALL
# =====================================================================

def display_all_sales():
    """Fetches and displays all contents of the table in the console."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM coffee_shop_sales")
        rows = cursor.fetchall()
        
        if not rows:
            print("\nThe table is currently empty.")
            return False
            
        column_headers = [i[0] for i in cursor.description]
        
        print("\n" + "="*80)
        print(" | ".join(column_headers))
        print("="*80)
        for row in rows:
            print(" | ".join(str(item) for item in row))
        print("="*80)
        return True
    except Error as e:
        print(f"\n[ERROR] Failed to fetch data: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def export_to_csv(file_name="coffee_sales_export.csv"):
    """Executes SELECT * and outputs all table content into a clean CSV file."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM coffee_shop_sales")
        rows = cursor.fetchall()
        
        column_headers = [i[0] for i in cursor.description]
        
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_headers)
            writer.writerows(rows)
            
        print(f"\n[SUCCESS] Export successful! Saved to '{file_name}'.")
    except Error as e:
        print(f"\n[ERROR] Export Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# 4. CHART VISUALIZATION (Seaborn)
# =====================================================================

def chart_visualisation():
    """Fetches sales data and renders charts using Seaborn."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee_shop_sales")
        rows = cursor.fetchall()
        column_headers = [i[0] for i in cursor.description]

        if not rows:
            print("\nThe table is currently empty. Nothing to visualize.")
            return

        df = pd.DataFrame(rows, columns=column_headers)

        # Derive a revenue column for richer charts
        if "transaction_qty" in df.columns and "unit_price" in df.columns:
            df["revenue"] = df["transaction_qty"] * df["unit_price"]

        print("\n--- Chart Options ---")
        print("a. Revenue by Product Category (bar chart)")
        print("b. Quantity Sold by Store Location (bar chart)")
        print("c. Unit Price Distribution (histogram)")
        print("d. Revenue by Product Category per Store (grouped bar chart)")
        chart_choice = input("Choose a chart (a-d): ").strip().lower()

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        if chart_choice == 'a' and "product_category" in df.columns and "revenue" in df.columns:
            summary = df.groupby("product_category")["revenue"].sum().sort_values(ascending=False).reset_index()
            sns.barplot(data=summary, x="product_category", y="revenue", palette="viridis")
            plt.title("Revenue by Product Category")
            plt.xlabel("Product Category")
            plt.ylabel("Total Revenue")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_revenue_by_category.png"

        elif chart_choice == 'b' and "store_location" in df.columns and "transaction_qty" in df.columns:
            summary = df.groupby("store_location")["transaction_qty"].sum().sort_values(ascending=False).reset_index()
            sns.barplot(data=summary, x="store_location", y="transaction_qty", palette="magma")
            plt.title("Quantity Sold by Store Location")
            plt.xlabel("Store Location")
            plt.ylabel("Total Quantity Sold")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_quantity_by_location.png"

        elif chart_choice == 'c' and "unit_price" in df.columns:
            sns.histplot(df["unit_price"], bins=20, kde=True, color="teal")
            plt.title("Unit Price Distribution")
            plt.xlabel("Unit Price")
            plt.ylabel("Frequency")
            out_file = "chart_unit_price_distribution.png"

        elif chart_choice == 'd' and "product_category" in df.columns and "store_location" in df.columns and "revenue" in df.columns:
            summary = df.groupby(["store_location", "product_category"])["revenue"].sum().reset_index()
            sns.barplot(data=summary, x="store_location", y="revenue", hue="product_category")
            plt.title("Revenue by Product Category per Store")
            plt.xlabel("Store Location")
            plt.ylabel("Total Revenue")
            plt.xticks(rotation=45, ha="right")
            plt.legend(title="Product Category", bbox_to_anchor=(1.05, 1), loc="upper left")
            out_file = "chart_revenue_by_category_per_store.png"

        else:
            print("\n[INVALID INPUT] Unrecognized chart option or missing required columns.")
            plt.close()
            return

        plt.tight_layout()
        plt.savefig(out_file, dpi=150)
        plt.close()
        print(f"\n[SUCCESS] Chart saved to '{out_file}'.")

    except Error as e:
        print(f"\n[ERROR] Chart Visualization Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# =====================================================================
# INTERACTIVE USER OPTION CONSOLE
# =====================================================================
def user_interface_menu():
    # Make sure table is built before showing the menu
    manage_table_structure()
    
    while True:
        print("\n" + " COFFEE SHOP DATABASE CONTROL PANEL ".center(50, "="))
        print("1. Add New Sale Transaction")
        print("2. Update Transaction Quantity")
        print("3. Delete Sale Transaction")
        print("4. View All Sales (SELECT *)")
        print("5. Export Database Rows to CSV File")
        print("6. Generate Chart Visualisation (Seaborn)")
        print("7. Exit Terminal Application")
        print("=" * 50)
        
        choice = input("Enter your selection (1-7): ").strip()
        
        if choice == '1':
            print("\n--- Enter Sale Record Details ---")
            date = input("Transaction Date (YYYY-MM-DD): ")
            time = input("Transaction Time (HH:MM:SS): ")
            qty = int(input("Transaction Quantity: "))
            store_id = int(input("Store ID: "))
            loc = input("Store Location: ")
            prod_id = int(input("Product ID: "))
            price = float(input("Unit Price: "))
            cat = input("Product Category: ")
            p_type = input("Product Type: ")
            detail = input("Product Detail Summary: ")
            
            insert_sale(date, time, qty, store_id, loc, prod_id, price, cat, p_type, detail)
            
        elif choice == '2':
            print("\n--- Update Transaction Record ---")
            t_id = int(input("Enter target Transaction ID to alter: "))
            new_qty = int(input("Enter new numerical quantity: "))
            update_sale_quantity(t_id, new_qty)
            
        elif choice == '3':
            print("\n--- Remove Transaction Record ---")
            t_id = int(input("Enter target Transaction ID to drop: "))
            confirm = input(f"Are you completely sure you want to drop ID {t_id}? (y/n): ").lower()
            if confirm == 'y':
                delete_sale(t_id)
            else:
                print("Operation aborted.")
                
        elif choice == '4':
            display_all_sales()
            
        elif choice == '5':
            file_out = input("Enter output filename (Press Enter for default 'coffee_sales_export.csv'): ")
            if file_out.strip() == "":
                export_to_csv()
            else:
                export_to_csv(file_out.strip())
                
        elif choice == '6':
            chart_visualisation()

        elif choice == '7':
            print("\nShutting down control application loop. Goodbye!")
            break
        else:
            print("\n[INVALID INPUT] Selection out of boundaries. Choose an index from 1 to 7.")

if __name__ == "__main__":
    user_interface_menu()