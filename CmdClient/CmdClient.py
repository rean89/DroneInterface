from DroneConnection import DroneConnection

drone = DroneConnection()

print("### Drone test client ###")

while True:

    if not drone.isConnected():
        print("# connect..")
        while not drone.isConnected():
            drone.connect()

        print("# Enter '?' for help")

    userInput = input("# Command:\n")
    userInput.lower()

    # Close client.
    if userInput == "exit":
        break

    # Raw input from the left and right control stick.
    elif userInput == "raw":
        print("# Enter raw data.")
        data = input("Data: ")
        drone.sendData(data)

    # Set throttle, yaw, roll and pitch
    elif userInput == "rc":
        print("# Enter values for throttle, yaw, roll & pitch.")
        throttle = input("Throttle: ")
        yaw = input("Yaw: ")
        roll = input("Roll: ")
        pitch = input("Pitch: ")
        drone.sendRC(throttle, yaw, roll, pitch)

    # Set GPS.
    elif userInput == "gps":
        print("# Enter latitude & longitude of the new GPS position")
        latitude = input("Latitude: ")
        longitude = input("Longitude: ")
        drone.setGPS(latitude, longitude)

    # Get telemetry information.
    elif userInput == "tele":
        drone.requestTelemetry()

    # Show help
    elif userInput == "?" or userInput == "help":
        print("<cmd>,<value>,<value>,...")
        print("Commands | Values")
        print("raw      | Enter raw data.")
        print("rc       | throttle, yaw, roll, pitch")
        print("gps      | latitude & longitude; Set a new GPS position.")
        print("tele     | Telemetry information.")
        print("connect  | Try to connect to the drone.")
        print("exit     | Close client.")

    # Invalid input
    else:
        print("Invalid input.")


drone.disconnect()
print("Connection colsed.")
input()
