from GpsChecker import GpsComparer
from GpsDecimalDegree import GpsCoord
from Drone import Drone

drone = Drone()
comparer = GpsComparer()

# Tolerance in meters.
tolerance = 10

# Main loop
while True:

        dronePos = drone.reqGPS()
        targetPos = GpsCoord(0.0, 0.0)

        if gpsData is not None:# and comparer.getDistance(targetPos, dronePos) < tolerance:
            pass
