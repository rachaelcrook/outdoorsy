"""

This app.py file contains all the logic for command line arguments being passed as well running interactively
from the command line.

To run interactively, run outdoorsy from the command line without flags.

To run the program with arguments run outdoorsy with the necessary flags to either upload a new file to the database,
view the current DB output with option flags to sort by name(default) or vehicle_type.

To see all command line arguments, run:
outdoorsy -h

Examples:

To upload a csv to the database:
outdoorsy -f /folder/file.csv -d comma

To upload comma or pipe delimited file to database at specified location:
outdoorsy -f /folder/file.csv -d comma -db /opt/database

To view entries in the database sorted by Vehicle Type:
outdoorsy -v -s vehicle_type

To view entries in the database at specified location, sorted by Full Name:
outdoorsy -v -s name -db /opt/database

To run in interactive mode:
outdoorsy

"""

import os
from os.path import exists
import sqlite3
from tabulate import tabulate
from .database import get_entries, create_table, insert_csv_to_db
from colorama import Fore, Style
import argparse

# The version specified here is used in pyproject.toml for the package's version uploaded to pypi
# and in the --version argparse argument below
__version__ = '0.0.19'


def create_parser():
    """Creates the Argument Parser Object and
        adds all the required arguments to it.

        Returns:
            Parser

        """
    # create a parser object
    parser = argparse.ArgumentParser(prog="outdoorsy",
                                     add_help=True,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""
***Outdoorsy***
Command Line tool for displaying Outdoorsy user information from a local database.

***Features***
-Use as command-line tool interactively or by passing arguments
-Creates a local SQL Lite Database for storing files
-View database in a table format from the command-line
-Sort by "Name" or "Vehicle Type" columns (from sample files)

Please see examples at the end of this help page or visit the project's github for more information.
https://github.com/rachaelcrook/outdoorsy""",
                                     epilog="""
                                     
***Examples***

Run in interactive mode:
outdoorsy
                                     
Upload CSV file to database:
outdoorsy -f C:\\folder\\file.csv -d comma

Upload Pipe delimited file to database:
outdoorsy -f C:\\folder\\pipes.text -d pipe

View data that has previously been uploaded to the database:
outdoorsy -v

View data sorted by Vehicle Type:
outdoorsy -v -s vehicle_type

View data sorted by name:
outdoorsy -v -s name """)

    # Defining arguments
    file_group = parser.add_argument_group(title="options - Upload a new file.")
    file_group.add_argument("-f", "--file",
                            required=False,
                            help="Full path to file")

    file_group.add_argument("-d", "--delimiter",
                            choices=['comma', 'pipe'],
                            required=False,
                            help="File's delimiter")

    file_group.add_argument("-db", "--dbpath",
                            required=False,
                            help="Path to create database. Defaults to current directory")

    view_group = parser.add_argument_group(title="options - View and Sort data")

    view_group.add_argument("-v", "--view",
                            required=False, action='store_true',
                            help="View the Outdoorsy Customer Table.")

    view_group.add_argument("-s", "--sort",
                            choices=['name', 'vehicle_type'],
                            required=False,
                            help="Sort the database table by the Outdoorsy Customer's Fullname or Vehicle Type")

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    return parser


def parse_args(args):
    # Creating the parser and parsing the arguments
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    return parsed_args


def run_interactively():
    menu = '''
    Welcome to the Outdoorsy interface.
    
    Please select one of the following options:
    1) Upload new file (comma or pipe delimited)
    2) View entries
    3) Exit.
    
    
    Your selection:  '''

    # using walrus operator to ask for user input directly in the while loop.
    while (user_input := input(menu)) != "3":
        if user_input == "1":
            input_path = input("Enter the path to the comma or pipe delimited file you would like to upload: ")
            input_delimiter = input('Enter the delimiter "comma" or "pipe" : ').lower()
            delimiter = parse_delimiter(input_delimiter)
            input_dbpath_option = input('Would you like to specify the DB Path? (Y/n): ').lower()
            if input_dbpath_option == "y":
                input_dbpath = input("Enter the path to create the Database: ")
                if exists(input_dbpath):
                    try:
                        dbpath = os.path.join(input_dbpath, "customers.db")
                        create_table(dbpath)
                        insert_csv_to_db(input_path, delimiter, dbpath)
                        print(Fore.GREEN + f"File Uploaded successfully! Database is located at: "
                                           f"{dbpath}")
                        print(Style.RESET_ALL)
                    except FileNotFoundError:
                        print(Fore.RED + f"no comma or pipe delimited files were found at that path. Path entered was:"
                                         f" {input_path} Please verify a comma or pipe delimited file exists"
                                         f" at this path and try again.")
                        print(Style.RESET_ALL)
                    except sqlite3.OperationalError:
                        print(Fore.RED + f"The path specified was not found. Please try again. Path: {input_dbpath}")
                        print(Style.RESET_ALL)

                    except TypeError:
                        print(Fore.RED + f"The delimiter specified must be either comma or pipe."
                                         f" The delimiter entered was: {input_delimiter} Please try again.")
                        print(Style.RESET_ALL)
                else:
                    print(Fore.RED + f"Error: The path specified to create the database does not exist. Please"
                                     f"try again using a valid path. Path entered was: {input_dbpath}")
                    print(Style.RESET_ALL)

            elif input_dbpath_option == "n":
                try:
                    create_table()
                    insert_csv_to_db(input_path, delimiter)
                    print(Fore.GREEN + f"File Uploaded successfully! Database is located in "
                                       f"the current working directory: {os.getcwd()}")
                    print(Style.RESET_ALL)

                except FileNotFoundError:
                    print(Fore.RED + f"no comma or pipe delimited files were found at that path. Path entered was:"
                                     f" {input_path} Please verify a comma or pipe delimited file exists"
                                     f" at this path and try again.")
                    print(Style.RESET_ALL)
                except TypeError:
                    print(Fore.RED + f"The delimiter specified must be either comma or pipe."
                                     f" The delimiter entered was: {input_delimiter} Please try again.")
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + f"Please specify 'y' to specify the path to create the database or 'n' "
                                 f"to default to the current directory.")
                print(Style.RESET_ALL)
        elif user_input == "2":
            custom_db_path = input("Did you previously set a custom DB Path? (Y/n): ").lower()
            if custom_db_path == "y":
                input_dbpath = input("Please enter path to database: ")
                dbpath = os.path.join(input_dbpath, "customers.db")
                if exists(dbpath):
                    select_info = input("Would you like to sort by Full Name (1) or by Vehicle Type (2)?  (1|2): ")
                    if select_info == "1":
                        # dbpath = os.path.join(input_dbpath, "customers.db")
                        create_table(dbpath)
                        results = get_entries('name', dbpath)
                        print(format_results(results))
                    elif select_info == "2":
                        results = get_entries('vehicle_type', dbpath)
                        print(format_results(results))
                    else:
                        print(Fore.RED + "Invalid option, please try again!")
                        print(Style.RESET_ALL)
                else:
                    print(Fore.RED + f"Error: Unable to locate database at path: {dbpath}. Please try again! ")
                    print(Style.RESET_ALL)
            elif custom_db_path == "n":
                select_info = input("Would you like to sort by Full Name (1) or by Vehicle Type (2)?  (1|2): ")
                if select_info == "1":
                    results = get_entries('name')
                    print(format_results(results))
                elif select_info == "2":
                    results = get_entries('vehicle_type')
                    print(format_results(results))
                else:
                    print(Fore.RED + "Invalid option, please try again!")
                    print(Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid option, please try again!")
                print(Style.RESET_ALL)

        elif user_input == "3":
            break
        else:
            print(Fore.RED + "Invalid option, please try again!")
            print(Style.RESET_ALL)


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

The parse_delimiter function is referenced when a delimiter is specified either with a 
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


if __name__ == "__main__":
    run_interactively()
