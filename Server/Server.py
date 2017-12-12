import os
import socket
if os.name != "nt":
    import fcntl
    import struct

"""
Handles the connection to the remote control.
"""
class DroneServer:

    def __init__(self):

        # Connection to the remote control.
        self.__rcConnection = []

        # Address of the remote control.
        self.__rcAddress = []

        # Is a remote control connected?
        self.__rcConnected = False

        # Only one remote control at a time allowed.
        self.__maxClients = 1

        # IP address of the server.
        self.__ipAddress = self.getIP()

        # Port of the socket connection.
        self.__port = 8000

        # Address of the server.
        self.__serverAddress = (self.__ipAddress, self.__port)

        # Socket for the connection.
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    """
    Start the server.
    """
    def start(self):
        self.__socket.bind(self.__serverAddress)
        self.__socket.listen(self.__maxClients)
        print("# Server started.")


    """
    Stop the server.
    """
    def stop(self):
        # Close connection an clear variables.
        self.__rcConnection.close()
        self.__rcConnection = []
        self.__rcAddress = []
        self.__rcConnected = False


    """
    Send data to the remote control.
    """
    def sendData(self, data):
        # Check rc connection state.
        if self.__rcConnected:
            try:
                # Try to send data to the rc.
                self.__rcConnection.sendall(data)
                print("# Data send to rc.")

            except Exception, error:
                print("# Error sending data to rc: ", str(error))


    """
    Get data from the remote control.
    """
    def getData(self):
        # Check rc connection state.
        if self.__rcConnected:
            try:
                # Try to get data from the rc.
                data = self.__rcConnection.recv(1024)
                return data

            except Exception, error:
                print("# Error getting data from rc: ", str(error))


    """
    Search for a remote control.
    """
    def searchRC(self):
        # Check rc connection state.
        if not self.__rcConnected:
            try:
                # Wait for a remote control to connect.
                self.__rcConnection, self.__rcAddress = self.__socket.accept()
                self.__rcConnected = True

            except Exception, error:
                print("# Error searching for rc: ", str(error))


    """
    Is a remote control connected?
    """
    def isRcConnected(self):
        return self.__rcConnected


    """
    Returns the ip address of the interface.
    """
    def _getInterfaceIP(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])


    """
    Get the local ip address.
    """
    def _getIP(self):
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            interfaces = [
                "eth0",
                "eth1",
                "eth2",
                "wlan0",
                "wlan1",
                "wifi0",
                "ath0",
                "ath1",
                "ppp0",
                ]
            for ifname in interfaces:
                try:
                    ip = self._getInterfaceIP(ifname)
                    break
                except IOError:
                    pass
        return ip
