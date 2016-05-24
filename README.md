# geolocation
Playing with Python, Flask, and IP2Location 

## Getting Started
Go to http://lite.ip2location.com/ and download a data file with lat/log into a folder named `data` at the root of the project. This should be all you need, and then you can call the following...

## Contract for v1

### Details
This call will provide geolocation details for a given properly formatted and publicly routable IP address in IPv4 or IPv6 formats.

**Verb:** GET

**Path:** `/api/v1/details/<any_public_ip>`    

**Responses:**

#### HTTP 200 - Successful
**Description:** In the event that the address provided is correctly formatted and is _publicly_ routable.

**Example:**

- `<provided_ip>`: "8.8.8.8", "173.199.5.15"
    
**Result:**    
```
{
    "ipAddress": "8.8.8.8",
    "countryCode": "US",
    "countryName": "United States",
    "longitude": -122.07851409912,
    "latitude": 37.405990600586,
    "cityName": "Mountain View",
    "regionName": "California"
}
```

#### HTTP 404 - Failed
**Description:** In the event that the address provided is correctly formatted and is _privately_ routable.

**Example:** (for `<provided_ip>`) 

- 10.0.0.0 - 10.255.255.255 (10.0.0.0/8)
- 172.16.0.0 - 172.31.255.255 (172.16.0.0/12)
- 192.168.0.0 - 192.168.255.255 (192.168.0.0/16)

**Result:**
```
{
    "ipAddress": "<provided_ip>",
    "errorCode": "InvalidAddressRange",
    "errorMessage": "The address ’<provided_ip>’ is not a publicly routable address. Only publicly routable IPv4 and IPv6 formats are supported."
}
```

#### HTTP 400 - Failed
**Description:** In the event that the address provided is correctly formatted and is _privately_ routable. 

**Example:** (for `<provided_ip>`) "10.0.1", "10.0.0.0/32"

**Result:**
```
{
    "ipAddress": "<provided_ip>",
    "errorCode": "InvalidAddressFormat",
    "errorMessage": "The address ’<provided_ip>’ is not in a recognized format. Only publicly routable IPv4 and IPv6 formats are supported."
}
```

#### HTTP 500 - Failed
**Description:** In the event that backend resources are unavailable or some other fatal scenario occured.

**Example:** (value doesn't matter)

**Result:**
```
{
    "ipAddress": "<provided_ip>",
    "errorCode": "ServerError",
    "errorMessage": "The address could not be evaluated due to a server side issue."
}
```

