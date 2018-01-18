from DroneConnection import DroneConnection

import csv
try:
    # For Python 2.x
    from StringIO import StringIO
except ImportError:
    # For Python 3.x
    from io import StringIO

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
    elif userInput == "set rc":
        print("# Enter values for throttle, yaw, roll & pitch.")
        throttle = input("Throttle: ")
        yaw = input("Yaw: ")
        roll = input("Roll: ")
        pitch = input("Pitch: ")
        drone.sendRC(throttle, yaw, roll, pitch)

    # Set GPS.
    elif userInput == "set wp":
        print("# Enter a new way point.")
        wpNo = input("WP number: ")
        lat = input("Latitude: ")
        lon = input("Longitude: ")
        altHold = input("AltHold: ")
        heading = input("Heading: ")
        timeStay = input("Time to stay: ")
        flag = input("Nav flag: ")
        drone.setGPS(wpNo, lat, lon, altHold, heading, timeStay, flag)

    elif userInput == "set gps":
        print("# Enter raw gps values.")
        fix = input("Fix: ")
        numSat = input("NumSat: ")
        lat = input("Lat: ")
        lon = input("Lon: ")
        attitude = input("Attitude: ")
        speed = input("Speed: ")
        drone.sendRawGPS(fix, numSat, lat, lon, attitude, speed)

    elif userInput == "set misc":
        print("# Enter new misc values.")
        powerTrigger = input("Power trigger: ")
        minThrottle = input("Min throttle: ")
        maxThrottle = input("Max throttle: ")
        minCmd = input("Min command: ")
        failsafeThrottle = input("Failsafe throttle: ")
        arm = input("Arm: ")
        lifetime = input("Lifetime: ")
        mag = input("Mag: ")
        vbatScale = input("Vbat scale: ")
        vbatWarn1 = input("Vbat warn lvl 1: ")
        vbatWarn2 = input ("Vbat warn lvl 2: ")
        vbatCrit = input("Vbat crit: ")
        drone.sendMisc(powerTrigger, minThrottle, maxThrottle, minCmd, failsafeThrootle, arm, lifetime, mag, vbatScale, vbatWarn1, vbatWarn2, vbarCrit)

    elif userInput == "calib mag":
        drone.calibMag()

    elif userInput == "calib acc":
        drone.calibAcc()

    elif userInput == "get raw":
        print("# Enter raw data.")
        data = input("Data: ")
        print(drone.recData(data))

    # Get telemetry information.
    elif userInput == "get imu":
        droneData = drone.recIMU()
        reader = csv.reader(StringIO(droneData), delimiter=";")
        for row in reader:
            try:
                numVal = []
                for num in row:
                    numVal.append(float(num))
                print("+----------+------------+---------------+---------------+")
                print("|  Sensor  |\tX\t|\tY\t|\tZ\t|")
                print("+----------+------------+---------------+---------------+")
                print("|   Accel  |\t", "{0:.2f}".format(numVal[1] / 512), "g\t|\t", "{0:.2f}".format(numVal[2] / 512), " g\t|\t", "{0:.2f}".format(numVal[3] /512) + "g\t|")
                print("|   Gyro   |\t" + str(numVal[4]) + "\t|\t" + str(numVal[5]) + "\t|\t" +str(numVal[6]) + "\t|")
                print("|   Mag    |\t" + str(numVal[7]) + "|\t" + str(numVal[8]) + "\t|\t" +str(numVal[9]) + "\t|")
                print("+----------+------------+---------------+---------------+")
                print("")
            except Exception as error:
                print("Error converting data:" + str(error))

    elif userInput == "get ident":
        print(drone.recIdent())

    elif userInput == "get status":
        print(drone.recStatus())

    elif userInput == "get rc":
        print(drone.recRC())

    elif userInput == "get wp":
        print(drone.recWP())

    elif userInput == "get gps":
        print(drone.recRawGPS())

    elif userInput == "get comp gps":
        print(drone.recCompGPS())

    elif userInput == "get attitude":
        print(drone.recAttitude())

    elif userInput == "get altitude":
        print(drone.recAltitude())

    elif userInput == "get analog":
        print(drone.recAnalog())

    elif userInput == "get misc":
        print(drone.recMisc())

    elif userInput == "get motor":
        print(drone.recMotor())

    elif userInput == "get pid":
        print(drone.recPID())

    # Show help
    elif userInput == "?" or userInput == "help":
        print("<cmd>,<value>,<value>,...")
        print("Commands     | Values")
        print("raw          | Enter raw data.")
        print("set rc       | throttle, yaw, roll, pitch")
        print("set gps      | set GPS")
        print("set wp       | Set a new way point; latitude & longitude.")
        print("set misc     | set misc.")
        print("calib acc    | Calibrate accel. sensor.")
        print("calib mag    | Calibrate mag. sensor.")

        print("get raw      | Enter raw data and rec data.")
        print("get ident    | Ident the drone.")
        print("get status   | Status of the drone")
        print("get rc       | get rc value")
        print("get wp       | get wp")
        print("get gps      | get raw gps")
        print("get comp gps | get comp gps")
        print("get imu      | Get the imu values.")
        print("get attitude | get attitude")
        print("get altitude | get altitude")
        print("get analog   | get analog")
        print("get misc     | get misc")
        print("get motor    | motor0-4")
        print("get pid      | get pid")
        print("connect      | Try to connect to the drone.")
        print("exit         | Close client.")

    # Invalid input
    else:
        print("Invalid input.")


drone.disconnect()
print("Connection colsed.")
input()
