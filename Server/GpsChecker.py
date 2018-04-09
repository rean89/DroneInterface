import math

class GpsComparer:

    __EARTH_RADIUS = 6371000


    def __init__(self):
        pass

    """
    Expects two GPS coords in dd format.
    Uses the Haversine formular to calculate the distance.
    Returns the distance in meters.
    """
    def getDistance(self, tar, pos):
        rLatTar = math.radians(tar.getLat())
        rLatPos = math.radians(pos.getLat())

        rDeltaLat = math.radians(pos.getLat() - tar.getLat())
        rDeltaLon = math.radians(pos.getLon() - tar.getLon())

        a = math.sin(rDeltaLat / 2) * math.sin(rDeltaLat / 2) + math.cos(rLatTar) * math.cos(rLatPos) * math.sin(rDeltaLon / 2) * math.sin(rDeltaLon / 2);

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));

        return self.__EARTH_RADIUS * c;


    """
    Compare the heading.
    Returns the offset between the headings.
    """
    def getRotationOffset(self, rotationInfo1, rotationInfo2):
        pass
