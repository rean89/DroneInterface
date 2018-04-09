import csv
try:
    # For Python 2.x
    from StringIO import StringIO
except ImportError:
    # For Python 3.x
    from io import StringIO


class CsvConverter:


    def __init__(self):
        pass

    """
    Send data to the multiwii board.
    """
    def toList(self, rcData):

        reader = csv.reader(StringIO(rcData.decode('utf-8')), delimiter=";")
        for row in reader:
            try:
                numbVal = []
                for numb in row:
                    numbVal.append(float(numb))

            except Exception, error:
                return ""
                print("# Error reading data: ", error)
            finally:
                return numbVal

    def toCSV(self, data):
        for value in droneData:
            csvData += str(float(value)) + ";"
        csvData = csvData[0:len(csvData) - 1]
        return csvData
