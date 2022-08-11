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

import sys
from .app import run_interactively, format_results, parse_delimiter, parse_args, InvalidDelimiter
from .database import get_entries, insert_csv_to_db


def main():
    if len(sys.argv) == 1:
        # Run interactively if no arguments are passed.
        run_interactively()

    args = parse_args(sys.argv[1:])
    print(sys.argv)

    if args.file and args.delimiter:
        input_path = args.file
        delimiter = parse_delimiter(args.delimiter)
        insert_csv_to_db(input_path, delimiter)

    if args.delimiter and not args.file:
        print("Please specify both a file and delimiter. For example: python cli.py -f comma.csv -d comma")

    if args.view and not args.sort:
        results = get_entries('name')
        print(format_results(results))

    if args.view and args.sort:
        sorted_by = args.sort
        if sorted_by == 'name':
            results = get_entries('name')
            print(format_results(results))
        elif sorted_by == 'vehicle_type':
            sorted_by = "vehicle_type"
            results = get_entries(sorted_by)
            print(format_results(results))
        else:
            print("Invalid option, please try again!")
