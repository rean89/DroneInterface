#from pymultiwii import MultiWii
from MultiWiiSerialProtocol import MSP

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
            #self.__board = MultiWii(self.__rpi3BSerialPortAddress)
            self.msp = MSP(self.__rpi3BSerialPortAddress)
        else:
            #self.__board = MultiWii(self.__rpiOldSerialPortAddress)
            self.msp = MSP(self.__rpiOldSerialPortAddress)


    """
    Send data to the multiwii board.
    """
    def sendData(self, rcData):

        reader = csv.reader(StringIO(rcData.decode('utf-8')), delimiter=";")
        for row in reader:
            try:
                csvData = ""
                numbVal = []
                cmd = int(row[0])
                for numb in row:
                    numbVal.append(float(numb))
                if cmd >= 200 and cmd < 300:
                    # Send a command to the flight controller.
                    print("Send data to fc...")
                    self.msp.sendData(cmd, numbVal[1:len(numbVal)])
                elif cmd >= 100 and cmd < 200:
                    # Request info from the flight conroller.
                    droneData = self.msp.getData(cmd)

                    # Convert to csv format.
                    csvData += str(cmd) + ";"
                    for value in droneData:
                        csvData += str(float(value)) + ";"
                    csvData = csvData[0:len(csvData) - 1]
                else:
                    print("# Invalid command or data.")
            except Exception, error:
                return "0"
                print("# Error reading data: ", error)
            finally:
                return csvData


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
