# outdoorsy
```
A demo command line tool for displaying information from a comma or tab delimited file.

usage: cli.py [-h] [-f FILE] [-d {comma,pipe}] [-v VIEW] [-s {name,vehicle_type}]

Outdoorsy Command Line tool for displaying Outdoorsy user information. Visit https://github.com/rachaelcrook/outdoorsy for more information

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify a new file to be uploaded to the Database. For example, C:\folder\file.csv Note: file needs to be either comma or pipe delimited
  -d {comma,pipe}, --delimiter {comma,pipe}
                        To upload a file to the Database, specify the delimiter used in the file
  -v VIEW, --view VIEW  View the Outdoorsy Customer Table from the Database. Sorted by Fullname by Default
  -s {name,vehicle_type}, --sort {name,vehicle_type}
                        Sort the database table by the Outdoorsy Customer's Fullname or Vehicle Type
                       
```
