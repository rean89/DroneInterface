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
        # Wait for data from rc and send it to the flight controller.
        rcData = server.getData()
        print("# RC data: ", str(rcData))

        droneData = str(drone.sendData(rcData))
        print("# Drone data: ", str(droneData.decode('utf-8')))

        if not droneData == "":
            # Send recevied data from the drone to the rc.
            server.sendData(droneData)



# Done. Stop the server.
server.stop()
print("# Server stopped.")
