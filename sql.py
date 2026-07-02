import csv
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # safe backend for non-interactive/terminal use
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================================
# CONNECTION CONFIG
# =====================================================================
# NOTE: update these to match your local MySQL setup.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'H@rshit1234',
    'database': 'diwalisales'
}

TABLE_NAME = "`diwali sales data`"  # backticks required: name contains spaces

def get_connection():
    """Establishes and returns a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# =====================================================================
# 1. TABLE STRUCTURE MANAGEMENT (DDL)
# =====================================================================

def manage_table_structure():
    """Creates the diwali sales data table if it doesn't already exist.

    The original SQL dump did not define a primary key, which makes
    targeted UPDATE/DELETE operations unsafe (no way to address a single
    row). A `row_id` auto-increment primary key is added here purely for
    CRUD purposes; it does not appear in the original dump's columns.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        create_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            row_id INT AUTO_INCREMENT PRIMARY KEY,
            User_ID INT DEFAULT NULL,
            Cust_name TEXT,
            Product_ID TEXT,
            Gender TEXT,
            `Age Group` TEXT,
            Age INT DEFAULT NULL,
            Marital_Status INT DEFAULT NULL,
            State TEXT,
            Zone TEXT,
            Occupation TEXT,
            Product_Category TEXT,
            Orders INT DEFAULT NULL,
            Amount INT DEFAULT NULL,
            Status TEXT,
            unnamed1 TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        cursor.execute(create_query)
        print("Table 'diwali sales data' verified/created successfully.")

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

def insert_sale(user_id, cust_name, product_id, gender, age_group, age,
                 marital_status, state, zone, occupation, product_category,
                 orders, amount, status, unnamed1=""):
    """Inserts a new record using parameterized queries to prevent SQL injection."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"""
        INSERT INTO {TABLE_NAME}
        (User_ID, Cust_name, Product_ID, Gender, `Age Group`, Age,
         Marital_Status, State, Zone, Occupation, Product_Category,
         Orders, Amount, Status, unnamed1)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (user_id, cust_name, product_id, gender, age_group, age,
                 marital_status, state, zone, occupation, product_category,
                 orders, amount, status, unnamed1)

        cursor.execute(query, data)
        connection.commit()
        print(f"\n[SUCCESS] Data added! Inserted row_id: {cursor.lastrowid}")
    except Error as e:
        print(f"\n[ERROR] Insert Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_sale_amount(row_id, new_amount):
    """Updates the Amount for a specific row_id."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"UPDATE {TABLE_NAME} SET Amount = %s WHERE row_id = %s"
        cursor.execute(query, (new_amount, row_id))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"\n[SUCCESS] Data updated! Affected rows: {cursor.rowcount}")
        else:
            print(f"\n[WARNING] No record found with row_id: {row_id}")
    except Error as e:
        print(f"\n[ERROR] Update Failed: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_sale(row_id):
    """Deletes a record based on its row_id."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = f"DELETE FROM {TABLE_NAME} WHERE row_id = %s"
        cursor.execute(query, (row_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"\n[SUCCESS] Data deleted! Affected rows: {cursor.rowcount}")
        else:
            print(f"\n[WARNING] No record found with row_id: {row_id}")
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

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()

        if not rows:
            print("\nThe table is currently empty.")
            return False

        column_headers = [i[0] for i in cursor.description]

        print("\n" + "="*100)
        print(" | ".join(column_headers))
        print("="*100)
        for row in rows:
            print(" | ".join(str(item) for item in row))
        print("="*100)
        return True
    except Error as e:
        print(f"\n[ERROR] Failed to fetch data: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def export_to_csv(file_name="diwali_sales_export.csv"):
    """Executes SELECT * and outputs all table content into a clean CSV file."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
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

        cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        rows = cursor.fetchall()
        column_headers = [i[0] for i in cursor.description]

        if not rows:
            print("\nThe table is currently empty. Nothing to visualize.")
            return

        df = pd.DataFrame(rows, columns=column_headers)

        print("\n--- Chart Options ---")
        print("a. Total Amount by State (bar chart)")
        print("b. Total Orders by Product Category (bar chart)")
        print("c. Age Distribution (histogram)")
        print("d. Total Amount by Zone per Gender (grouped bar chart)")
        chart_choice = input("Choose a chart (a-d): ").strip().lower()

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        if chart_choice == 'a' and "State" in df.columns and "Amount" in df.columns:
            summary = df.groupby("State")["Amount"].sum().sort_values(ascending=False).reset_index()
            sns.barplot(data=summary, x="State", y="Amount", palette="viridis")
            plt.title("Total Amount by State")
            plt.xlabel("State")
            plt.ylabel("Total Amount")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_amount_by_state.png"

        elif chart_choice == 'b' and "Product_Category" in df.columns and "Orders" in df.columns:
            summary = df.groupby("Product_Category")["Orders"].sum().sort_values(ascending=False).reset_index()
            sns.barplot(data=summary, x="Product_Category", y="Orders", palette="magma")
            plt.title("Total Orders by Product Category")
            plt.xlabel("Product Category")
            plt.ylabel("Total Orders")
            plt.xticks(rotation=45, ha="right")
            out_file = "chart_orders_by_category.png"

        elif chart_choice == 'c' and "Age" in df.columns:
            sns.histplot(df["Age"].dropna(), bins=20, kde=True, color="teal")
            plt.title("Age Distribution")
            plt.xlabel("Age")
            plt.ylabel("Frequency")
            out_file = "chart_age_distribution.png"

        elif chart_choice == 'd' and "Zone" in df.columns and "Gender" in df.columns and "Amount" in df.columns:
            summary = df.groupby(["Zone", "Gender"])["Amount"].sum().reset_index()
            sns.barplot(data=summary, x="Zone", y="Amount", hue="Gender")
            plt.title("Total Amount by Zone per Gender")
            plt.xlabel("Zone")
            plt.ylabel("Total Amount")
            plt.xticks(rotation=45, ha="right")
            plt.legend(title="Gender", bbox_to_anchor=(1.05, 1), loc="upper left")
            out_file = "chart_amount_by_zone_gender.png"

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
        print("\n" + " DIWALI SALES DATABASE CONTROL PANEL ".center(55, "="))
        print("1. Add New Sale Record")
        print("2. Update Sale Amount")
        print("3. Delete Sale Record")
        print("4. View All Sales (SELECT *)")
        print("5. Export Database Rows to CSV File")
        print("6. Generate Chart Visualisation (Seaborn)")
        print("7. Exit Terminal Application")
        print("=" * 55)

        choice = input("Enter your selection (1-7): ").strip()

        if choice == '1':
            print("\n--- Enter Sale Record Details ---")
            user_id = int(input("User ID: "))
            cust_name = input("Customer Name: ")
            product_id = input("Product ID: ")
            gender = input("Gender: ")
            age_group = input("Age Group (e.g. 26-35): ")
            age = int(input("Age: "))
            marital_status = int(input("Marital Status (0 = Single, 1 = Married): "))
            state = input("State: ")
            zone = input("Zone: ")
            occupation = input("Occupation: ")
            product_category = input("Product Category: ")
            orders = int(input("Orders: "))
            amount = int(input("Amount: "))
            status = input("Status: ")

            insert_sale(user_id, cust_name, product_id, gender, age_group, age,
                        marital_status, state, zone, occupation, product_category,
                        orders, amount, status)

        elif choice == '2':
            print("\n--- Update Sale Record ---")
            r_id = int(input("Enter target row_id to alter: "))
            new_amount = int(input("Enter new Amount: "))
            update_sale_amount(r_id, new_amount)

        elif choice == '3':
            print("\n--- Remove Sale Record ---")
            r_id = int(input("Enter target row_id to drop: "))
            confirm = input(f"Are you completely sure you want to drop row_id {r_id}? (y/n): ").lower()
            if confirm == 'y':
                delete_sale(r_id)
            else:
                print("Operation aborted.")

        elif choice == '4':
            display_all_sales()

        elif choice == '5':
            file_out = input("Enter output filename (Press Enter for default 'diwali_sales_export.csv'): ")
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