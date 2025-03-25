import requests
import json

def populate_stop_dict(line):
    STOPS_URL = "https://api-v3.mbta.com/stops?filter[route]=" + line
    stops = requests.get(url=STOPS_URL).json()["data"]

    stops_dict = {}

    for i, stop in enumerate(stops):
        name = stop["attributes"]["name"]
        stops_dict[name] = i

    with open('stops.txt', 'a') as stops_file: 
        stops_file.write(json.dumps(stops_dict))
        stops_file.write('\n')