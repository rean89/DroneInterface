from Server import DroneServer
from Drone import Drone

drone = Drone()

# Create the server and start it.
server = DroneServer()
server.start()

# Main loop
while True:
    if not server.isRcConnected():
        print("# Waiting for rc to connect..")
        server.searchRC()
        print("# Connected to rc.")

    if server.isRcConnected():
        data = server.getData()
        drone.sendData(data)

        decodedData = str(data.decode('utf-8'))
        print("Data: ", decodedData)

        if decodedData[:2] == "3;":
            dummyMsg = "Dummy tele info answer."
            server.sendData(dummyMsg.encode('utf-8'))


# Done. Stop the server.
server.stop()
print("# Server stopped.")
