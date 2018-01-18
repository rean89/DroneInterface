import socket


"""
Setup a communication with the drone.
Send remote control commands, GPS positions or
receive telemetry informations from the drone.
"""
class DroneConnection:

    # Message ids of the MultiWii serial portocol
    __IDENT = 100
    __STATUS = 101
    __RAW_IMU = 102
    __SERVO = 103
    __MOTOR = 104
    __RC = 105
    __RAW_GPS = 106
    __COMP_GPS = 107
    __ATTITUDE = 108
    __ALTITUDE = 109
    __ANALOG = 110
    __RC_TUNING = 111
    __PID = 112
    __BOX = 113
    __MISC = 114
    __MOTOR_PINS = 115
    __BOXNAMES = 116
    __PIDNAMES = 117
    __WP = 118
    __BOXIDS = 119
    __SET_RAW_RC = 200
    __SET_RAW_GPS = 201
    __SET_PID = 202
    __SET_BOX = 203
    __SET_RC_TUNING = 204
    __ACC_CALIBRATION = 205
    __MAG_CALIBRATION = 206
    __SET_MISC = 207
    __RESET_CONF = 208
    __SET_WP = 209
    __SWITCH_RC_SERIAL = 210
    __IS_SERIAL = 211
    __DEBUG = 254


    def __init__(self):
        # Connection state.
        self.connected = False
        # IP address and port of the drone server.
        self.server_address = ('192.168.0.105', 8000)
        # Create a socket for the connection.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    """
    Connect with the drone.
    """
    def connect(self):
        # Already connected?
        if not self.connected:
            try:
                # Try to connect and update the connection state.
                self.sock.connect(self.server_address)
                self.connected = True
            except Exception as e:
                #print("Exception: ", e)
                pass


    """
    Disconnect from the drone.
    """
    def disconnect(self):
        # Check the connection state.
        if self.connected:
            # Close the connection.
            self.sock.close()
            self.connected = False


    """
    Get connection state.
    """
    def isConnected(self):
        # Return connection state.
        return self.connected


    """
    Set the values for throttle, yaw, roll and pitch.
    """
    def sendRC(self, throttle, yaw, roll, pitch):
        # Connected to the drone?
        if self.isConnected:
            # Create the data package.
            cmd = (str(self.__SET_RAW_RC) + ";" + str(throttle) + ";"
                        + str(yaw) + ";" + str(roll) + ";" + str(pitch))
            try:
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    """
    Set a GPS way point?.
    """
    def sendWP(self, wpNo, lat, lon, altHold, heading, timeStay, navFlag):
        # Connected to the drone?
        if self.connected:
            # Create the command.
            cmd = (str(self.__SET_WP) + ";" + str(wpNo) + ";" + str(lat)
                        + ";" + str(lon) + ";" + str(altHold)+ ";"
                        + str(heading) + ";" + str(timeStay) + ";"
                        + str(navFlag))
            try:
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    """
    Set a GPS way point?.
    """
    def sendGPS(self, fix, numSat, lat, lon, attitude, speed):
        # Connected to the drone?
        if self.connected:
            # Create the command.
            cmd = (str(self.__SET_WP) + ";" + str(fix) + ";" + str(numSat)
                        + ";" + str(lat) + ";" + str(lon)+ ";" + str(attitude)
                        + ";" + str(speed))
            try:
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    """
    Set a GPS way point?.
    """
    def sendMisc(self, powerTrigger, minThrottle, maxThrottle, minCmd, failsafeThrootle, arm, lifetime, mag, vbatScale, vbatWarn1, vbatWarn2, vbatCrit):
        # Connected to the drone?
        if self.connected:
            # Create the command.
            cmd = (str(self.__SET_WP) + ";" + str(powerTrigger) + ";"
                    + str(minThrottle) + ";" + str(maxThrottle) + ";"
                    + str(minCmd)+ ";" + str(failsafeThrootle) + ";"
                    + str(arm) + ";" + str(lifetime) + ";"
                    + str(mag) + ";" + str(vbatScale) + ";"
                    + str(vbatWarn1) + ";" + str(vbatWarn2) + ";"
                    + str(vbatCrit))
            try:
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    """
    Request telemetry information of the drone.
    """
    def recIMU(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__RAW_IMU)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recIdent(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__IDENT)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    def recStatus(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__STATUS)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recAnalog(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__ANALOG)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recMisc(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__MISC)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recRawGPS(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__RAW_GPS)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recCompGPS(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__COMP_GPS)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recWP(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__WP)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recPID(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__PID)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recRC(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__RC)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recAttitude(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__ATTITUDE)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recAltitude(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__ALTITUDE)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    def recMotor(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            try:
                cmd = str(self.__MOTOR)
                # Send the command.
                self.sock.sendall(cmd.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    """
    Send raw data to the server.
    """
    def sendData(self, rawData):
        if self.isConnected:
            try:
                # Send the data.
                self.sock.sendall(rawData.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)

    """
    Send raw data to the server.
    """
    def recData(self, rawData):
        if self.isConnected:
            try:
                # Send the data.
                self.sock.sendall(rawData.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                return data.decode('utf-8')
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)
