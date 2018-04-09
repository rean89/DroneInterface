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
    TUNING = 111
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
    SET_TUNING = 204
    CALIB_ACC = 205
    CALIB_MAG = 206
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
        self.cmdStructDic[str(self.IDENT)] = '3BI'
        self.cmdStructDic[str(self.STATUS)] = '3HIB'
        self.cmdStructDic[str(self.IMU)] = '9h'
        self.cmdStructDic[str(self.SERVO)] = '8H'
        self.cmdStructDic[str(self.MOTOR)] = '8H'
        self.cmdStructDic[str(self.RC)] = '8H'
        self.cmdStructDic[str(self.GPS)] = '2B2I3H'
        self.cmdStructDic[str(self.COMP_GPS)] = '2HB'
        self.cmdStructDic[str(self.ATTITUDE)] = '3h'
        self.cmdStructDic[str(self.ALTITUDE)] = 'ih'
        self.cmdStructDic[str(self.ANALOG)] = 'B3H'
        self.cmdStructDic[str(self.TUNING)] = '7B'
        # self.cmdStructDic[str(self.PID)] = '30B'
        # self.cmdStructDic[str(self.BOX)] = ''
        self.cmdStructDic[str(self.MISC)] = '6HIH4B'
        self.cmdStructDic[str(self.MOTOR_PINS)] = '8B'
        # self.cmdStructDic['116'] = 's'
        # self.cmdStructDic['117'] = 's'
        self.cmdStructDic[str(self.WP)] = '2B3I3HB'
        # self.cmdStructDic['119'] = ''
        # self.cmdStructDic['120'] = ''
        self.cmdStructDic[str(self.NAV_STATUS)] = '5BH'
        self.cmdStructDic[str(self.NAV_CONFIG)] = '2B5HB2HBHB'
        self.cmdStructDic[str(self.SET_RC)] = '8H'
        self.cmdStructDic[str(self.SET_GPS)] = '2B2I2H'
        # self.cmdStructDic['203'] = ''
        # self.cmdStructDic['204'] = ''
        self.cmdStructDic[str(self.SET_TUNING)] = '7B'
        self.cmdStructDic[str(self.CALIB_ACC)] = ''
        self.cmdStructDic[str(self.CALIB_MAG)] = ''
        self.cmdStructDic[str(self.SET_MISC)] = '6HIH4B'
        self.cmdStructDic[str(self.RESET_CONFIG)] = ''
        self.cmdStructDic[str(self.SET_WP)] = 'B3I2HB'
        self.cmdStructDic[str(self.SELECT_SETTING)] = 'B'
        self.cmdStructDic[str(self.SET_HEAD)] = 'H'
        # self.cmdStructDic['212'] = ''
        self.cmdStructDic[str(self.SET_MOTOR)] = '8H'
        self.cmdStructDic[str(self.SET_NAV_CONFIG)] = '2B5HB2HBHB'


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

        try:
            self.serialPort.open()
        except Exception, error:
            print("# Error opening serial port on '" + serialAddr + "'.")

    def sendData(self, cmd, data):
        crc = self.getCRC(cmd, data)
        if cmd >= IDENT and cmd < SET_RC:
            dataStruct = ""
            dataPackage = self.preamblePkg + [0, cmd, crc]
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
                    # Read the rest of the preamble + direction sign.
                    self.serialPort.read(len(self.preamblePkg) - 1)
                    break
            dataLength = struct.unpack('<B', self.serialPort.read())[0]
            data = self.serialPort.read(dataLength + 2)
            unpackedData = struct.unpack('<B' + self.cmdStructDic[str(cmd)] + 'B', data)

        except Exception, error:
            # Something went wrong.
            print("# Error getting data from fc: ", error)
        finally:
            # Clean up.
            self.serialPort.flushInput()
            self.serialPort.flushOutput()
            # Remove checksum from data pkg.
            return unpackedData[1:len(unpackedData) - 2]

    def getCRC(self, cmd, data):
        if cmd >= IDENT and cmd < RC:
            pkg = struct.pack('<BB', *[cmd, 0])
        else:
            dataLength = struct.calcsize(self.cmdStructDic[str(cmd)])
            dataPkg = [cmd, dataLength] + data
            pkg = struct.pack('<BB' + self.cmdStructDic[str(cmd)], *dataPkg)
        crc = 0
        for i in pkg:
            crc = crc ^ ord(i)
        return crc
