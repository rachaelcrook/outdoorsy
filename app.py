from database import get_entries, create_table, format_results, insert_csv_to_db, parse_delimiter

menu = '''Please select one of the following options:
1) Upload new file (comma or pipe delimited)
2) View entries
3) Exit.


Your selection:  '''

welcome = "Welcome to the Outdoorsy Interface"
create_table()


# using walrus operator to ask for user input directly in the while loop.
while (user_input := input(menu)) != "3":
    if user_input == "1":
        input_path = input("Enter the path to the comma or tab delimited file you would like to upload: ")
        input_delimiter = input('Enter the delimiter "comma" or "tab" : ')
        delimiter = parse_delimiter(input_delimiter)
        insert_csv = insert_csv_to_db(input_path, delimiter)

    elif user_input == "2":
        select_info = input("Would you like to sort by Full Name (1) or by Vehicle Type (2)?  (1|2): ")
        if select_info == "1":
            results = get_entries('name')
            print(format_results(results))
        elif select_info == "2":
            sorted_by = "vehicle_type"
            results = get_entries(sorted_by)
            print(format_results(results))
        else:
            print("Invalid option, please try again!")

    else:
        print("Invalid option, please try again!")
