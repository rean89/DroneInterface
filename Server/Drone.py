from pymultiwii import MultiWii

import csv
try:
    # For Python 2.x
    from StringIO import StringIO
except ImportError:
    # For Python 3.x
    from io import StringIO


class Drone:
                            
    # Serial port address for older models then rpi 3b?
    __rpiOldSerialPortAddress = "/dev/ttyAMA0"

    # Serial port address for the rpi 3b
    __rpi3BSerialPortAddress = "/dev/ttyS0"

    def __init__(self):

        self.__debug = True
        revisionId = self._getRpiRevision()
        if revisionId == "a02082" or revisionId == "a22082":
            self.__board = MultiWii(self.__rpi3BSerialPortAddress)
        else:
            self.__board = MultiWii(self.rpiOldSerialPortAddress)

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


    """
    Get revision of the RPi.
    """
    def _getRpiRevision(self):
        # Extract board revision from cpuinfo file
        revision = "0000"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[:8] == 'Revision':
                    revision = line[11:len(line) - 1]
        except:
            revision = "0000"
        finally:
            f.close()
            return revision
