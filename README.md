# geolocation
Playing with Python, Flask, and IP2Location 

## Getting Started
Go to http://lite.ip2location.com/ and download a data file with lat/log into a folder named `data` at the root of the project. This should be all you need, and then you can call the following...

- `/distance/<any_public_ip>`   - _for distance information between the given IP and the AWS regions, sorted shortest to longest_
- `/distance/server`            - _for distance information between the service's IP and the AWS regions, sorted shortest to longest_
- `/distance`                   - _for distance information between Google's DNS and the AWS regions, sorted shortest to longest_
