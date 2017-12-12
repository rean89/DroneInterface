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

        revId = self._getRPiRev()
        # Check if RPi 3b or another revision.
        if revId == "a02082" or revId == "a22082":
            self.__board = MultiWii(self.__rpi3BSerialPortAddress)
        else:
            self.__board = MultiWii(self.__rpiOldSerialPortAddress)

    """
    Send data to the multiwii board.
    """
    def sendData(self, rawData):

        reader = csv.reader(StringIO(rawData.decode('utf-8')), delimiter=";")
        for row in reader:
            try:
                returnData = ""
                numbVal = []
                cmd = int(row[0])
                for numb in row:
                    numbVal.append(float(numb))
                #numbVal = [list(map(int, x)) for x in row]
                #cmd = numbVal[0]
                dataLength = len(numbVal) - 1
                if cmd >= 200 and cmd < 300:
                    # Send a command to the flight controller.
                    self.__board.sendCMD(dataLength, cmd, numbVal[1:dataLength])
                elif cmd >= 100 and cmd < 200:
                    returnData += str(cmd) + ";"
                    # Request info from the flight conroller.
                    #dataDic = self.__board.getData(cmd)
                    dataDic = self.__board.rawIMU
                    for key, value in dataDic.iteritems():
                        returnData += str(value) + ";"
                    returnData = returnData[0:len(returnData) - 1]
                else:
                    print("# Invalid command or data.")
            except Exception, error:
                print("# Error reading data: ", error)
            finally:
                return returnData

    """
    Get revision of the RPi.
    """
    def _getRPiRev(self):
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
