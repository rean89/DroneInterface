from DroneConnection import DroneConnection

drone = DroneConnection()

print("### Drone test client ###")



while True:

    if not drone.isConnected():
        print("# connect..")
        drone.connect()
        print("# Enter '?' for help")
    userInput = input("# Command:\n")

    # Close client.
    if userInput == "exit":
        break

    # Raw input from the left and right control stick.
    elif userInput[:6] == "RAW RC":
        print("# Enter the raw values of the left & right control stick.")
        lx = input("Lx: ")
        ly = input("Ly: ")
        rx = input("Rx: ")
        ry = input("Ry: ")
        drone.sendRawRC(lx, ly, rx, ry)

    # Set throttle, yaw, roll and pitch
    elif userInput[:2] == "RC":
        print("# Enter values for throttle, yaw, roll & pitch.")
        throttle = input("Throttle: ")
        yaw = input("Yaw: ")
        roll = input("Roll: ")
        pitch = input("Pitch: ")
        drone.sendRC(throttle, yaw, roll, pitch)

    # Set GPS.
    elif userInput[:3] == "GPS":
        print("# Enter latitude & longitude of the new GPS position")
        latitude = input("Latitude: ")
        longitude = input("Longitude: ")
        drone.setGPS(latitude, longitude)

    # Get telemetry information.
    elif userInput[:4] == "Tele":
        drone.requestTelemetry()

    # Show help
    elif userInput == "?":
        print("<cmd>,<value>,<value>,...")
        print("Commands | Values")
        print("RAW RC   | Lx, Ly, Rx, Ry; L & R control stick.")
        print("RC       | throttle, yaw, roll, pitch")
        print("GPS      | latitude & longitude; Set a new GPS position.")
        print("Tele     | Telemetry information.")
        print("exit     | Close client.")

    # Invalid input
    else:
        print("Invalid input.")


drone.disconnect()
print("Connection colsed.")
input()
