import json
from pprint import pprint
from operator import itemgetter


def readJsonCoordinates(uri):
    """Reads a json in the given directory and returns the result in a array.
    uri -- the place in filesystem, where the file is stored
    """
    data = json.load(open(uri))
    coordinates = data['coordinates']
    pprint('initial coordinates: \n{}'.format(coordinates))
    if 'sequence' in coordinates[0]:
        print('a sequence was given -> Ordering the entries.')
        coordinates = sorted(coordinates, key=itemgetter('sequence'))
    else:
        print('Read no sequence data -> Ordering coordinates as given.')
    return coordinates


# usage
coordinates = readJsonCoordinates('Files/coordinatesSequence.json')
# use the long and lat attributes
for idx, station in enumerate(coordinates):
    print('{}. station for Drone -> long: {} | lat: {}'.format(
        idx, station['latitude'], station['longitude']))
