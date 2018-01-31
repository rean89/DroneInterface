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

    # RPi revision id's.
    __RPI_3B_UK_ID = "a02082"
    __RPI_3B_JAP_ID = "a32082"
    __RPI_3B_EMB_ID = "a22082"
    __RPI_ZERO_W_ID = "9000c1"

    # Serial address for RPi's older then 3. generation.
    __rpiOldSerialPortAddress = "/dev/ttyAMA0"

    # Serial address for 3. generation RPi's.
    __rpi3BSerialPortAddress = "/dev/ttyS0"

    __debug = False

    def __init__(self):

        revId = self._getRPiRev()

        # Check if 3. generation RPi.
        if (revId == self.__RPI_3B_UK_ID or revId == self.__RPI_3B_JAP_ID
            or revId == self.__RPI_3B_EMB_ID or revId == self.__RPI_ZERO_W_ID):
            self.msp = MSP(self.__rpi3BSerialPortAddress)
        else:
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
