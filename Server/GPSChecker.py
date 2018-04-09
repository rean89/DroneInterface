import math

class GpsComparer:

    # Message id's of the multiwii serial protocol
    __EARTH_RADIUS = 6371000



    def __init__(self, serialAddr):


    """
    Expects two GPS coords in dd format.
    Uses the Haversine formular to calculate the distance.
    Returns the distance in meters.
    """
    def getDistance(self, coord1, coord2):
        p1 = (coord1.getLon() - coord2.getLon()) * math.cos(0.5 * (coord1.getLat() + coord2.getLat()))
        p2 = (coord1.getLat() - coord2.getLat())
        """
        hypot(x,y) = sqrt(x * x + y * y)
        """
        return self.__EARTH_RADIUS * math.hypot(p1, p2)



    """
    Compare the heading.
    Returns the offset between the headings.
    """
    def getRotationOffset(self, rotationInfo1, rotationInfo2):
