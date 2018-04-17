
class GpsCoord:

    def __init__(self, lat, lon):
        self.__lat = lat
        self.__lon = lon
        self.__alt = 173.6  # decimal meter value of heilbronn. should be dynamically setted

    def getLat(self):
        return self.__lat

    def getLon(self):
        return self.__lon

    def getAlt(self):
        return self.__alt
