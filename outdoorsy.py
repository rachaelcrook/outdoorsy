import os
import csv
import re

# path = 'C:\\Users\\rcroo\\PycharmProjects\\outdoorsy\\commas.txt'


def csv_dict_list(path, delimiter):
    field_names = ['First Name', 'Last Name', 'Email', 'Vehicle Type', 'Vehicle Name', 'Vehicle Length']
    csv_dict_list = []
    with open(path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=field_names, delimiter=delimiter)
        for row in reader:
            row['Vehicle Length'] = re.sub("\D+", " ft", row['Vehicle Length'])
            csv_dict_list.append(row)
        return csv_dict_list

# newdict = csv_dict_list(path, ',')
#
# # print(newdict)