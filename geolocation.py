import json
import IP2Location

from flask import *
from netaddr import *
from operator import itemgetter
from collections import OrderedDict
from json import load
from urllib2 import urlopen
from math import radians, cos, sin, asin, sqrt

# Load Flask
app = Flask(__name__)

# Load IP2Location
location = IP2Location.IP2Location()
location.open("data/IP2LOCATION-LITE-DB11.BIN")


# Predefine a list of AWS regions achieved by dns lookup of EC2 endpoint URL hosts
datacenters = {
    'us-east-1': "207.171.162.181",
    'us-west-1': "204.246.163.231",
    'us-west-2': "205.251.235.5",
    'eu-west-1': "178.236.7.129",
    'eu-central-1': "54.239.54.36",
    'ap-northeast-1': "27.0.1.68",
    'ap-southeast-1': "203.83.220.199",
    'ap-southeast-2': "54.240.195.144",
    'sa-east-1': "177.72.244.143"
}


def haversine(lon1, lat1, lon2, lat2):

    """
    Calculate the distance between two points on Earth taking curvature into account
    :param lon1: First endpoint's longitude
    :param lat1: First endpoint's latitude
    :param lon2: Second endpoint's longitude
    :param lat2: Second endpoint's latitude
    :return: Distance in kilometers
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


@app.route('/distance')
@app.route('/distance/<address>')
def distance(address=None):
    results = {}

    # Provide a local or default address to use if one was not provided
    if address == "server":
        address = load(urlopen('http://httpbin.org/ip'))['origin']
    if address is None:
        address = "8.8.8.8"

    # Provide feedback to user if the address given isn't a valid formatted address
    try:
        address = IPAddress(address)
    except Exception, e:
        results['error'] = e.message
        return Response(json.dumps(results), mimetype='application/json')

    # Provide feedback to user if the address given isn't a valid public address
    if address.is_private():
        results['error'] = "The address provided or detected is not a valid public IP address"
        return Response(json.dumps(results), mimetype='application/json')

    client = location.get_all(address)
    for region in datacenters.iterkeys():
        server = location.get_all(datacenters[region])
        results[region] = haversine(
            client.longitude,
            client.latitude,
            server.longitude,
            server.latitude
        )

    results = OrderedDict(sorted(results.iteritems(), key=itemgetter(1)))
    return Response(json.dumps(results), mimetype='application/json')


@app.route('/details')
@app.route('/details/<address>')
def details(address=None):
    results = {}

    # Provide a local or default address to use if one was not provided
    if address == "server":
        address = load(urlopen('http://httpbin.org/ip'))['origin']
    if address is None:
        address = "8.8.8.8"

    # Provide feedback to user if the address given isn't a valid formatted address
    try:
        address = IPAddress(address)
    except Exception, e:
        results['error'] = e.message
        return Response(json.dumps(results), mimetype='application/json')

    # Provide feedback to user if the address given isn't a valid public address
    if address.is_private():
        results['error'] = "The address provided or detected is not a valid public IP address"
        return Response(json.dumps(results), mimetype='application/json')

    address_details = location.get_all(address)
    results['ipAddress'] = address
    results['countryCode'] = address_details.country_short
    results['countryName'] = address_details.country_long
    results['cityName'] = address_details.city
    results['regionName'] = address_details.region

    return Response(json.dumps(results), mimetype='application/json')


if __name__ == '__main__':
    app.run()
