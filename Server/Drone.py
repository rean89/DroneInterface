from pymultiwii import MultiWii

import csv
try:
    # For Python 2.x
    from StringIO import StringIO
except ImportError:
    # For Python 3.x
    from io import StringIO


class Drone:

    __debugOutputLabels = [["RC", "Throttle", "Yaw", "Roll", "Pitch"],
                            ["GPS", "Latitude", "Longitude"],
                            ["Tele"]]
    def __init__(self):
        self.__debug = True
        self.__rpi3SerialPortAddress = "/dev/ttyS0"
        self.__board = MultiWii(self.__rpi3SerialPortAddress)


    """
    Send data to the multiwii board.
    """
    def sendData(self, rawData):

        reader = csv.reader(StringIO(rawData.decode('utf-8')), delimiter=";")
        for row in reader:
            try:
                numbVal = [list(map(int, x)) for x in row]
                cmd = numbVal[0]
                if cmd == 0:
                    self.__board.sendCMD(4, MultiWii.SET_RAW_RC, numbVal[1:4])
                elif cmd == 1:
                    self.__board.sendCMD(2, MultiWii.SET_GPS, numbVal[1:2])
                elif cmd == 2:
                    self.__board.sendCMD(0, MultiWii.RAW_IMU)
                else:
                    print("# Invalid data.")
            except Exception, error:
                print("# Error reading data: ", error)

    """
    Get data from the multiwii board.
    """
    def getData(self):
        pass

    
