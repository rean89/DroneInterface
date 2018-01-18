import serial
import struct

class MSP:

    # Message id's of the multiwii serial protocol
    IDENT = 100
    STATUS = 101
    IMU = 102
    SERVO = 103
    MOTOR = 104
    RC = 105
    GPS = 106
    COMP_GPS = 107
    ATTITUDE = 108
    ALTITUDE = 109
    ANALOG = 110
    RC_TUNING = 111
    # PID = 112
    # BOX = 113
    MISC = 114
    MOTOR_PINS = 115
    # BOX_NAMES = 116
    # PID_NAMES = 117
    WP = 118
    # BOX_IDS = 119
    # SERVO_CONFIG = 120
    NAV_STATUS = 121
    NAV_CONFIG = 122
    # CELLS = 130

    SET_RC = 200
    SET_GPS = 201
    # SET_PID = 202
    # SET_BOX = 203
    SET_RC_TUNING = 204
    ACC_CALIB = 205
    MAG_CALIB = 206
    SET_MISC = 207
    RESET_CONFIG = 208
    SET_WP = 209
    SELECT_SETTING = 210
    SET_HEAD = 211
    # SET_SERVO_CONFIG = 212
    SET_MOTOR = 214
    SET_NAV_CONFIG = 215
    # SET_ACC_TRIM = 239
    # ACC_TRIM = 240
    # BIND = 241
    # EEPROM_WRITE = 250
    # DEBUG_MSG = 253
    # DEBUG = 254


    def __init__(self, serialAddr):
        self.preamblePkg = ['$', 'M', '<']
        self.preamblePkgStruct = '3c2B'
        self.cmdStructDic = dict()
        self.cmdStructDic['100'] = '3BI'
        self.cmdStructDic['101'] = '3HIB'
        self.cmdStructDic['102'] = '9h'
        self.cmdStructDic['103'] = '8H'
        self.cmdStructDic['104'] = '8H'
        self.cmdStructDic['105'] = '8H'
        self.cmdStructDic['106'] = '2B2I3H'
        self.cmdStructDic['107'] = '2HB'
        self.cmdStructDic['108'] = '3h'
        self.cmdStructDic['109'] = 'ih'
        self.cmdStructDic['110'] = 'B3H'
        self.cmdStructDic['111'] = '7B'
        # self.cmdStructDic['112'] = '30B'
        self.cmdStructDic['114'] = '6HIH4B'
        self.cmdStructDic['115'] = '8B'
        # self.cmdStructDic['116'] = 's'
        # self.cmdStructDic['117'] = 's'
        self.cmdStructDic['118'] = '2B3I3HB'
        self.cmdStructDic['121'] = '5BH'
        self.cmdStructDic['122'] = '2B5HB2HBHB'
        self.cmdStructDic['200'] = '8H'
        self.cmdStructDic['201'] = '2B2I2H'
        self.cmdStructDic['204'] = '7B'
        self.cmdStructDic['205'] = ''
        self.cmdStructDic['206'] = ''
        self.cmdStructDic['207'] = '6HIH4B'
        self.cmdStructDic['208'] = ''
        self.cmdStructDic['209'] = 'B3I2HB'
        self.cmdStructDic['210'] = 'B'
        self.cmdStructDic['211'] = 'H'
        self.cmdStructDic['214'] = '8H'
        self.cmdStructDic['215'] = '2B5HB2HBHB'

        self.serialPort = serial.Serial()
        self.serialPort.port = serialAddr
        self.serialPort.baudrate = 115200
        self.serialPort.bytesize = serial.EIGHTBITS
        self.serialPort.parity = serial.PARITY_NONE
        self.serialPort.stopbits = serial.STOPBITS_ONE
        self.serialPort.timeout = 0
        self.serialPort.xonxoff = False
        self.serialPort.rtscts = False
        self.serialPort.dsrdtr = False
        # self.serialPort.writeTimeout = 2
        try:
            self.serialPort.open()
        except Exception, error:
            print("# Error opening serial port on '" + serialAddr + "'.")

    def sendData(self, cmd, data):
        crc = self.getCRC(cmd, data)
        if cmd >= 100 and cmd < 200:
            dataStruct = ""
            dataLength = 0
            dataPackage = self.preamblePkg + [dataLength, cmd, crc]
        else:
            dataStruct = self.cmdStructDic[str(cmd)]
            dataLength = struct.calcsize(self.cmdStructDic[str(cmd)])
            dataPackage = self.preamblePkg + [dataLength, cmd] + data
            dataPackage.append(crc)
        try:
            self.serialPort.write((struct.pack('<' + self.preamblePkgStruct
                                    + dataStruct  + 'B', *dataPackage)))
            """
            # To validate the API, check for a ACK from the flight controller.
            while True:
                print("Wait for ACK..")
                data = self.serialPort.read()
                if data == self.preamblePkg[0]:
                    # Read the rest of the preamble.
                    ack = self.serialPort.read(len(self.preamblePkg) - 1)
                    print("ACK: " + str(struct.unpack('<BB', ack)))
                    break
                else:
                    print("ACK: " + str(data))
            """
        except Exception, error:
            print("# Error sending data to fc: " + str(error) )


    def getData(self, cmd):
        unpackedData = []
        try:
            self.sendData(cmd, [])

            # Wait for preamble.
            while True:
                data = self.serialPort.read()
                if data == self.preamblePkg[0]:
                    # Read the rest of the preamble.
                    self.serialPort.read(len(self.preamblePkg) - 1)
                    break
            dataLength = struct.unpack('<B', self.serialPort.read())[0]
            self.serialPort.read()
            data = self.serialPort.read(dataLength)
            unpackedData = struct.unpack('<' + self.cmdStructDic[str(cmd)], data)
            print("Length: ", dataLength)
            print("Packed: ", data)
            print("Unpacked: ", unpackedData)
        except Exception, error:
            # Something went wrong.
            print("# Error getting data from fc: ", error)
        finally:
            # Clean up.
            self.serialPort.flushInput()
            self.serialPort.flushOutput()
            return unpackedData

    def getCRC(self, cmd, data):
        pkg = ""
        if cmd >= 100 and cmd < 200:
            pkg = struct.pack('<BB', *[cmd, 0])
        else:
            dataLength = struct.calcsize(self.cmdStructDic[str(cmd)])
            dataPkg = [cmd, dataLength] + data
            pkg = struct.pack('<BB' + self.cmdStructDic[str(cmd)], *dataPkg)
        crc = 0
        for i in pkg:
            crc = crc ^ ord(i)
        return crc
