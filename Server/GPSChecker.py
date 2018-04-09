import struct

class GpsComparer:

    # Message id's of the multiwii serial protocol
    EARTH_RADIUS = 100



    def __init__(self, serialAddr):


    """
    Expects two GPS coords in dd format.
    Returns the distance between the coords in meters.
    """
    def getDistance(self, coord1, coord2):



    """
    Compare the heading.
    Returns the offset between the headings.
    """
    def getRotationOffset(self, rotationInfo1, rotationInfo2):
