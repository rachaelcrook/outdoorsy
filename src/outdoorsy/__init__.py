"""

A demo command line tool for displaying information from a comma or pipe delimited file.

Features

- Use as command-line tool interactively or by passing arguments
- Creates a local SQL Lite Database for storing files
- View database in a table format from the command-line
- Sort by "Name" or "Vehicle Type" columns (from sample files)

Usage

outdoorsy can be used to extract info from a Comma or Pipe delimited file in two ways:

- Command line/Terminal tool ran interactively `outdoorsy`
- Command line/Terminal tool ran with arguments `outdoorsy -h`

https://github.com/rachaelcrook/outdoorsy


"""

# The InvalidDelimiter class below is imported in order for import references in tests to function,
# but is not used in this __init__.py file directly.
import os
import sys
from os.path import exists
from .app import run_interactively, format_results, parse_delimiter, parse_args, InvalidDelimiter
from .database import get_entries, insert_csv_to_db, create_table
from colorama import Fore, Style


def main():
    if len(sys.argv) == 1:
        # Run interactively if no arguments are passed.
        run_interactively()

    args = parse_args(sys.argv[1:])
    # if troubleshooting issues with parsing args, uncomment the line below to see what args are being captured
    # print(sys.argv)

    if args.file and args.delimiter and not args.dbpath:
        input_path = args.file

        # check if the file specified in the -f argument exists first, if not throw an error.
        file_exists = exists(input_path)
        if file_exists:
            create_table()
            delimiter = parse_delimiter(args.delimiter)
            try:
                insert_csv_to_db(input_path, delimiter)
                print(Fore.GREEN + f"File uploaded successfully ")
                print(Style.RESET_ALL)
            except TypeError:
                print(Fore.RED + f"Error: TypeError - Please verify {args.delimiter} is the correct "
                                 f"delimiter for this file type.")

        else:
            print(Fore.RED + f"Error: Could not find file at path:\n {input_path}."
                             f"\n Please verify the file exists and try again.")
            print(Style.RESET_ALL)

    if args.delimiter and not args.file:
        print(Fore.RED + "Please specify both a file and delimiter. For example: outdoorsy -f comma.csv -d comma")
        print(Style.RESET_ALL)

    if args.file and not args.delimiter:
        print(Fore.RED + "Please specify both a file and delimiter. For example: outdoorsy -f comma.csv -d comma")
        print(Style.RESET_ALL)

    if args.file and args.delimiter and args.dbpath:
        # check if the file specified in the -f argument exists first, if not throw an error.
        file_exists = exists(args.file)
        db_path_file_exists = exists(args.dbpath)

        if file_exists and db_path_file_exists:
            delimiter = parse_delimiter(args.delimiter)
            dbpath = os.path.join(args.dbpath, "customers.db")
            create_table(dbpath)
            insert_csv_to_db(args.file, delimiter, dbpath)
            print(Fore.GREEN + f"File uploaded successfully to Database at path: {args.dbpath}. \n"
                               f"Note: this database path will need to be specified everytime you would like to view"
                               f" the results. Otherwise, outdoorsy defaults to the current"
                               f" path which is {os.getcwd()} .")
            print(Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: Could either \n1. Not find the comma or pipe delimited file at the path specified"
                             f"\nor \n2. Not find the path specified to create the database.\n"
                             f" Please verify the file exists at {args.dbpath}"
                             f" and the path to create the database exists at {args.dbpath} "
                             f"  and try again.")
            print(Style.RESET_ALL)

    if args.view and not args.sort:
        results = get_entries('name')
        print(format_results(results))

    if args.sort and not args.view:
        print(Fore.RED + "Please specify both a view and sort argument. For example: outdoorsy -v -s vehicle_type")
        print(Style.RESET_ALL)

    if args.view and args.sort and not args.dbpath:
        sorted_by = args.sort
        if sorted_by == 'name':
            results = get_entries(sorted_by)
            print(format_results(results))
        elif sorted_by == 'vehicle_type':
            results = get_entries(sorted_by)
            print(format_results(results))
        else:
            print(Fore.RED + "Invalid option, please try again!")
            print(Style.RESET_ALL)

    if args.view and args.sort and args.dbpath:
        if exists(args.dbpath):
            sorted_by = args.sort
            if sorted_by == 'name':
                dbpath = os.path.join(args.dbpath, "customers.db")
                create_table(dbpath)
                results = get_entries(sorted_by, dbpath)
                print(format_results(results))
            elif sorted_by == 'vehicle_type':
                dbpath = os.path.join(args.dbpath, "customers.db")
                create_table(dbpath)
                results = get_entries(sorted_by, dbpath)
                print(format_results(results))
            else:
                print(Fore.RED + "Invalid option, please try again!")
                print(Style.RESET_ALL)
        else:
            print(Fore.RED + f"The path specified for the database path does not exist."
                             f" Please try again. path: {args.dbpath}")
            print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
