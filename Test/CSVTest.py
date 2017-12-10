import csv
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO

data = ("0;1;2;3;4")

f = StringIO(data)
reader = csv.reader(f, delimiter=';')

for row in reader:
    # Get the amount of entries in the row.
    print(len(row))
    # Access single entries in a row.
    print(row[0], row[1], row[2], row[3], row[4])
