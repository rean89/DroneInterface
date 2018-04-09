#from pymultiwii import MultiWii
from MultiWiiSerialProtocol import MSP

class Drone:

    __GPS_SCALE = 10000000

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

    def reqGPS(self):
        data = self.msp.getData(self.msp.GPS)
        GpsCoord
        if len(data) > 0:
            return GpsCoord(data[2] * self.__GPS_SCALE, data[3] * self.__GPS_SCALE)

    def reqRawAttitude(self):
        data = self.msp.getData(self.msp.ATTITUDE)
        if len(data) > 0:
            return data


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
