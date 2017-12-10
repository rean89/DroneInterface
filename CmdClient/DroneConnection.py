import socket


"""
Setup a communication with the drone.
Send remote control commands, GPS positions or
receive telemetry informations from the drone.
"""
class DroneConnection:

    def __init__(self):
        # Connection state.
        self.connected = False
        # IP address and port of the drone server.
        self.server_address = ('192.168.0.106', 8000)
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
                print("Exception:\n", e)


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
    Set a new GPS position.
    """
    def sendGPS(self, latitude, longitude):
        # Connected to the drone?
        if self.connected:
            # Create the command.
            command = "2;" + str(latitude) + ";" + str(longitude) + ";"
            try:
                # Send the command.
                self.sock.sendall(command.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    """
    Send the raw values of the left & right stick.
    """
    def sendRawRC(self, lx, ly, rx, ry):
        # Connected to the drone?
        if self.isConnected:
            # Create the data package.
            command = "0;" + str(lx) + ";" + str(ly) + ";" + str(rx) + ";" + str(ry) + ";"
            try:
                # Send the command.
                self.sock.sendall(command.encode('utf-8'))
            except Exception as e:
                print("Exception:\n", e)


    """
    Set the values for throttle, yaw, roll and pitch.
    """
    def sendRC(self, throttle, yaw, roll, pitch):
        # Connected to the drone?
        if self.isConnected:
            # Create the data package.
            command = "1;" + str(throttle) + ";" + str(yaw) + ";" + str(roll) + ";" + str(pitch) + ";"
            try:
                # Send the command.
                self.sock.sendall(command.encode('utf-8'))
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)


    """
    Request telemetry information of the drone.
    """
    def requestTelemetry(self):
        if self.isConnected:
            # Creat the command to request the telemetry information.
            command = "3;"
            try:
                # Send the command.
                self.sock.sendall(command.encode('utf-8'))
                # Wait for the telemetry information.
                data = self.sock.recv(1024)
                # Print the telemetry information.
                teleInfo = data.decode('utf-8')
                print(teleInfo)
            except Exception as e:
                # Handle exceptions.
                print("Exception:\n", e)
