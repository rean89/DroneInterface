from Server import DroneServer
from Drone import Drone

drone = Drone()

# Main loop
while True:

        gpsData = str(drone.reqRawGPS())

        if not droneData == "":
            # Check if in range.
            headingData = str(drone.reqCompGPS())
