import csv
import re
import sqlite3
from colorama import Fore, Style

"""
database.py contains the logic and functions to create a SQL Lite database (if it doesn't already exist) or connect
to the existing database. It is used by app.py when a new file is added or when the view option is selected.

"""


def create_table(db_path="customers.db"):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    with connection:
        connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS "customers" (
	"first_name" TEXT,
	"last_name"	TEXT,
	"email"	TEXT,
	"vehicle_type" TEXT,
	"vehicle_name" TEXT,
	"vehicle_length" INTEGER
); '''
        )


"""

The insert_csv_to_db function is referenced when a new comma or pipe delimited file is uploaded when running in 
command-line or interactive mode. It parses the file into a dictionary and then inserts the data in a SQL Lite database.
You could easily change the database to Postgres or another Database by editing the connections at the beginning of 
this file and if needed modifying the SQL statements in this function, create_table, and get_entries (in app.py).

To add support for files with other delimiters, such as tsv, do the following:
- The additional delimiter would need to be added to parse_delimiter and create_parser in app.py
- Any messages in app.py would need to be updated to reflect the additional option 
- Add additional test function to test_outdoorsy.py

"""


def insert_csv_to_db(path, delimiter, db_path="customers.db"):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    field_names = ['first_name', 'last_name', 'email', 'vehicle_type', 'vehicle_name', 'vehicle_length']
    with open(path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=field_names, delimiter=delimiter)

        for row in reader:
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            vehicle_type = row['vehicle_type']
            vehicle_name = row['vehicle_name']
            row['vehicle_length'] = re.sub("\D+", "", row['vehicle_length'])
            row['vehicle_length'] = int(row['vehicle_length'])
            vehicle_length = row['vehicle_length']

            with connection:
                connection.execute(
                    "INSERT INTO 'customers' VALUES (?, ?, ?, ?, ?, ?);",
                    (first_name, last_name, email, vehicle_type, vehicle_name, vehicle_length)
                )


def get_entries(sort_order, db_path="customers.db"):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()

    # since SQL parameters can't be used for anything other than values, this will be sorted in Python using the
    # if/else statement below instead. This is to avoid SQL injection.

    sql = "SELECT first_name, last_name, email, vehicle_type, vehicle_name, vehicle_length" \
          " FROM customers ORDER BY first_name, last_name asc;"
    try:
        cur.execute(sql)
        rows = cur.fetchall()

        # check if the user selected the option to sort by vehicle type or full name.
        if sort_order == "vehicle_type":
            sorted_list = sorted(rows, key=lambda row: row[3].lower())
        else:
            sorted_list = rows

    except sqlite3.OperationalError:
        print(Fore.RED + f"Table does not exist. Upload a new file first!")
        print(Style.RESET_ALL)
        return

    return sorted_list


if __name__ == '__main__':
    print("The database module should be imported, not ran directly.")
