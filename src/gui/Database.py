import sqlite3
from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st

from src import components


def _create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except sqlite3.Error as err:
        print(err)
    return connection


class Database:
    def __init__(self, db_file):
        self.connection = _create_connection(db_file)
        self.tables = [table[0] for table in self.connection.cursor().execute(
            "SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        self.current_option = ""

    def show_search(self):
        # Options
        self.current_option = st.selectbox("Select table to add data", self.tables)

        if self.current_option == "Customer":
            customer_id = datetime.now().strftime('%Y%m%d-%H%M%S-') + str(uuid4())
            customer_name = st.text_input("Input customer name: ", value="")
            if customer_name:
                data = components.Customer.search_by_name(self.connection, customer_name)
                df = pd.DataFrame(data.fetchall(), columns=['Customer ID', 'Customer name'])
                st.write(df)

        elif self.current_option == "Category":
            pass

        elif self.current_option == "Buyer":
            pass

        elif self.current_option == "Inventory":
            pass

        elif self.current_option == "Imports":
            pass

        elif self.current_option == "Transactions":
            pass

        elif self.current_option == "Item":
            pass

    def show_add(self):
        self.current_option = st.selectbox("Select table to search data", self.tables)

        if self.current_option == "Customer":
            customer_id = datetime.now().strftime('%Y%m%d-%H%M%S-') + str(uuid4())
            customer_name = st.text_input("Input customer name: ", value="")
            if st.button("Add customer"):
                check = components.Customer.insert(self.connection, customer_id, customer_name)
                if check is None:
                    st.write("Error!")
                else:
                    st.write("Customer added successfully!")

        elif self.current_option == "Category":
            pass

        elif self.current_option == "Buyer":
            pass

        elif self.current_option == "Inventory":
            pass

        elif self.current_option == "Imports":
            pass

        elif self.current_option == "Transactions":
            pass

        elif self.current_option == "Item":
            pass

    def show_remove(self):
        self.current_option = st.selectbox("Select table to search data", self.tables)

        if self.current_option == "Customer":
            input_value = st.text_input("Input customer id or name: ", value="")
            if st.button("Remove customer") and input != "":
                components.Customer.delete_by_id(self.connection, input_value)
                components.Customer.delete_by_name(self.connection, input_value)


        elif self.current_option == "Category":
            pass

        elif self.current_option == "Buyer":
            pass

        elif self.current_option == "Inventory":
            pass

        elif self.current_option == "Imports":
            pass

        elif self.current_option == "Transactions":
            pass

        elif self.current_option == "Item":
            pass

    def export_data(self, export_path):
        import csv

        try:
            for table in self.tables:
                # Export data into CSV file
                st.info(f"Exporting table '{table}'...\n")
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                with open(f"{export_path}/{table}.csv", "w+", encoding='utf-8') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter="\t")
                    csv_writer.writerow([i[0] for i in cursor.description])
                    csv_writer.writerows(cursor)
                st.success(f"Data exported Successfully into {export_path}/{table}.csv\n")

        except sqlite3.Error as err:
            print(err)
