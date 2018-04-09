from GpsChecker import GpsComparer
from GpsDecimalDegree import GpsCoord


myPosition = GpsCoord(49.133525, 8.548061)
myTownHall = GpsCoord(49.135941, 8.545129)

comparer = GpsComparer()

# Ca. 340m
print comparer.getDistance(myPosition, myTownHall)
