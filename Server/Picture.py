from PIL import Image
import piexif

from pprint import pprint

from GpsDecimalDegree import GpsCoord

picturePin = 0


#go further with https://gist.github.com/c060604/8a51f8999be12fc2be498e9ca56adc72

def addMetaData(image, uri):
    fileURL = 'Files/Images/exifTest.jpg'
    im = Image.open(fileURL)
    exif_dict = piexif.load(im.info["exif"])
    exif_dict["GPS"] = getGpsData()
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, fileURL)


def getGpsData():
    # retrun dict with correct tupel data
    return {
        piexif.GPSIFD.GPSLatitudeRef: "S",
        piexif.GPSIFD.GPSLatitude: [(40, 1), (41, 1), (476051999, 10000000)],
        piexif.GPSIFD.GPSLongitudeRef: "W",
        piexif.GPSIFD.GPSLongitude: [(165, 1), (22, 1), (14268000, 10000000)]
    }


def takePhoto():
    picturePin = 1
    # wait for file
    try:
        image = ""
        addMetaData(image, 'Files/Images/')
    except:
        Exception
        print('photo was not taken')
