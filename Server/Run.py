from GpsChecker import GpsComparer
from Drone import Drone

drone = Drone()

# Main loop
while True:

        gpsData = drone.reqRawGPS()
