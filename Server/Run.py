from GpsChecker import GpsComparer
from GpsDecimalDegree import GpsCoord
from Drone import Drone

drone = Drone()
comparer = GpsComparer()

# Tolerance in meters.
tolerance = 10

# Main loop
while True:

        dronePos = drone.reqRawGPS()
        targetPos = GpsCoord()

        if gpsData is not None:# and comparer.getDistance() < tolerance:
            pass
