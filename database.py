import csv
import re
import sqlite3
from tabulate import tabulate

connection = sqlite3.connect("customers.db")
connection.row_factory = sqlite3.Row


def parse_delimiter(delimiter):
    if delimiter == "comma":
        delimiter = ","
    elif delimiter == "pipe":
        delimiter = "|"
    return delimiter


def create_table():
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


def insert_csv_to_db(path, delimiter):
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


def get_entries(sort_order):
    cur = connection.cursor()
    # sort_order = user_input_sort

    # since SQL parameters can't be used for anything other than values, this will be sorted in Python using the
    # if/else statement below instead. This is to avoid SQL injection.

    sql = "SELECT first_name, last_name, email, vehicle_type, vehicle_name, vehicle_length" \
          " FROM customers ORDER BY first_name, last_name asc;"
    cur.execute(sql)
    rows = cur.fetchall()

    # check if the user selected the option to sort by vehicle type or full name.
    if sort_order == "vehicle_type":
        sorted_list = sorted(rows, key=lambda row: row[3])
    else:
        sorted_list = rows

    return sorted_list


# The format_result function is used to format the results returned from the database in a human-readable
# table format.
def format_results(results):
    table = tabulate(
        results,
        headers=['First Name', 'Last Name', 'Email', 'Vehicle Type', 'Vehicle Name', 'Vehicle Length (in FT.)'],
        tablefmt='psql')

    return table

