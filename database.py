import csv
import re
import sqlite3
from tabulate import tabulate

"""
database.py contains the logic and functions to create a SQL Lite database (if it doesn't already exist) or connect
to the existing database. It is used by app.py and cli.py when a new file is added or when the view option is selected.

"""

connection = sqlite3.connect("customers.db")
connection.row_factory = sqlite3.Row


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


"""

The insert_csv_to_db function is referenced when a new comma or pipe delimited file is uploaded when running in 
commandline or interactive mode. It parses the file into a dictionary and then inserts the data in a SQL Lite database.
You could easily change the database to PostGres or another Database by editing the connections at the beginning of 
this file and if needed modifying the SQL statements in this function, create_table, and get_entries.

If any changes are needed to support other file types such as tab delimited files, the additional delimiter would need
to be added to parse_delimiter in this file as well as create_parser in cli.py. 

Any messages in cli.py and app.py would need to be updated to reflect the additional option as well.
Lastly, a test function would need to be added to test_outdoorsy.py.

"""


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


"""

The format_result functions are used to format data returned from the database into a table displayed to the user
in a command line or terminal window. 

"""


def format_results(results):
    table = tabulate(
        results,
        headers=['First Name', 'Last Name', 'Email', 'Vehicle Type', 'Vehicle Name', 'Vehicle Length (in FT.)'],
        tablefmt='psql')

    return table


"""

Invalid Delimiter is a custom exception to be raised when an invalid delimited is specified when running interactively.
If an invalid delimiter is specified when running cli.py with arguments, an error message is returned automatically
via the argparse library.

"""


class InvalidDelimiter(Exception):
    pass


"""

The parse_delimiter function is referenced by cli.py and app.py when a delimiter is specified either with a 
command line argument or when running interactively. 

"""


def parse_delimiter(delimiter):
    if delimiter == "comma":
        delimiter = ","
    elif delimiter == "pipe":
        delimiter = "|"
    else:
        raise InvalidDelimiter

    return delimiter


if __name__ == '__main__':
    print("The database module should be imported, not ran directly.")
