from PIL import Image
import piexif
from fractions import Fraction
from pprint import pprint
import time
import datetime
from GpsDecimalDegree import GpsCoord

picturePin = 0


def to_deg(value, loc):
    """convert decimal coordinates into degrees, munutes and seconds tuple
    Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
    return: tuple like (25, 13, 48.343 ,'N')
    """
    print(value, loc)
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
    return (deg, min, sec, loc_value)


def change_to_rational(number):
    """convert a number to rantional
    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)


def addMetaData(image):
    exif_dict = piexif.load(image.info["exif"])
    # only until we get data from Drone
    mypos = GpsCoord(49.133525, 8.548061)
    exif_dict["GPS"] = parseGpsData(
        mypos.getLat(), mypos.getLon(), mypos.getAlt())
    # set heading to Photo
    exif_bytes = piexif.dump(exif_dict)
    # old
    #piexif.insert(exif_bytes, fileURI)
    saveUri = 'Files/Images/Out/out.jpg'
    image.save(saveUri, exif=exif_bytes)


def parseGpsData(lat, lng, altitude):
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(
        lat_deg[1]), change_to_rational(lat_deg[2]))
    exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(
        lng_deg[1]), change_to_rational(lng_deg[2]))

    return {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 1,
        piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude)),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exiv_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: exiv_lng,
        piexif.GPSIFD.GPSDateStamp: getDateStamp(),
    }


def getDateStamp():
    timestamp = time.time()
    print timestamp
    st = datetime.datetime.fromtimestamp(
        timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print st
    return st


def takePhoto():
    picturePin = 1
    # wait for file
    try:
      # not used yet
        image = Image.open('Files/Images/ExampleNiagaraFalls.JPG')
        addMetaData(image)
    except Exception as err:
        print('photo was not taken: \n{}'.format(err))


# usage
takePhoto()
