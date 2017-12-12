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
        data = server.getData()
        returnData = drone.sendData(data)

        rcData = str(data.decode('utf-8'))
        print("# RC data: ", rcData)

        if not returnData == "":
            droneData = str(returnData.decode('utf-8'))
            print("# Drone data: ", droneData)
            # Send recevied data from the drone to the rc.
            server.sendData(returnData)



# Done. Stop the server.
server.stop()
print("# Server stopped.")
