from DroneConnection import DroneConnection

import time
import csv
try:
    # For Python 2.x
    from StringIO import StringIO
except ImportError:
    # For Python 3.x
    from io import StringIO


def printIMU(data):
    reader = csv.reader(StringIO(data), delimiter=";")
    for row in reader:
        try:
            numVal = []
            for num in row:
                numVal.append(float(num))
            print("+----------+------------+---------------+---------------+")
            print("|  Sensor  |\tX\t|\tY\t|\tZ\t|")
            print("+----------+------------+---------------+---------------+")
            print("|   Accel  |\t" + str(numVal[1]) + "\t|\t" + str(numVal[2]) + "\t|\t" +str(numVal[3]) + "\t|")
            print("|   Gyro   |\t" + str(numVal[4]) + "\t|\t" + str(numVal[5]) + "\t|\t" +str(numVal[6]) + "\t|")
            print("|   Mag    |\t" + str(numVal[7]) + "\t|\t" + str(numVal[8]) + "\t|\t" +str(numVal[9]) + "\t|")
            print("+----------+------------+---------------+---------------+")
            print("")
        except Exception as error:
            print("Error converting data:" + str(error))

drone = DroneConnection()

print("### Drone test client ###")

while True:

    if not drone.isConnected():
        print("# connect..")
        while not drone.isConnected():
            drone.connect()

    printIMU(drone.recIMU())
    time.sleep(0.25)
