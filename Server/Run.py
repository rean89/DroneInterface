from Server import DroneServer
from Drone import Drone

drone = Drone()

# Create the server and start it.
server = DroneServer()
server.start()

# Main loop
while True:
    if not server.isRcConnected():
        server.searchRC()

    if server.isRcConnected():
        # Wait for data from rc and send it to the flight controller.
        rcData = server.getData()
        droneData = str(drone.sendData(rcData))

        if not droneData == "":
            # Send recevied data from the drone to the rc.
            server.sendData(droneData)
