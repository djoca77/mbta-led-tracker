import requests
import config
import constants
import time
import json

# Your MBTA API key
API_KEY = config.key

def populate_bits(line, stops):
    URL = "https://api-v3.mbta.com/vehicles?filter[route]=" + line + "&api_key=" + API_KEY
    vehicles = requests.get(url=URL).json()['data']

    out_bits = [0] * len(stops)

    for vehicle in vehicles:
        if vehicle["attributes"]["direction_id"] == constants.OUTBOUND:
            stop_id = str(vehicle["relationships"]["stop"]["data"]["id"])

            STOPS_URL = f"https://api-v3.mbta.com/stops/{stop_id}"
            stop_name = requests.get(url=STOPS_URL).json()['data']['attributes']['name']

            out_bits[(stops[stop_name])] = 1
    
    return out_bits
            

if __name__ == "__main__":
    lines = ["Blue", "Orange", "Red"]
    while 1:
        stop_dicts = open('stops.txt', 'r')

        for i, line in enumerate(stop_dicts):
            stop_dict = json.loads(line)
            populate_bits(lines[i], stop_dict)

        stop_dicts.close()

        time.sleep(30)

    
