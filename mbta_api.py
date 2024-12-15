import requests
import time
import json
import os
import serial
import time

import stops
import config
import constants

API_KEY = config.key

lineFlag = {"Orange":"o", "Blue":"b", "Red":"r", "Green":"g"}
lines = ["Blue", "Orange", "Red"]

def populate_bits(line, stops, arduino):
    URL = "https://api-v3.mbta.com/vehicles?filter[route]=" + line + "&api_key=" + API_KEY
    vehicles = requests.get(url=URL).json()['data']

    out_bits = [0] * len(stops)

    for vehicle in vehicles:
        if vehicle["attributes"]["direction_id"] == constants.NORTHBOUND:
            stop_id = str(vehicle["relationships"]["stop"]["data"]["id"])

            STOPS_URL = f"https://api-v3.mbta.com/stops/{stop_id}"
            stop_name = requests.get(url=STOPS_URL).json()['data']['attributes']['name']

            out_bits[(stops[stop_name])] = 1

    binary_string = ''.join(map(str, out_bits))
    output = lineFlag[line] + binary_string + '\n'
    print(output)

    # Send the bytes serially
    arduino.write(output.encode())
            

if __name__ == "__main__":
    arduino = serial.Serial('/dev/ttyACM0', '9600')
    time.sleep(2)

    if not os.path.exists('stops.txt'):
        stops.populate_stop_dict()

    while 1:
        stop_dicts = open('stops.txt', 'r')

        for i, line in enumerate(stop_dicts):
            stop_dict = json.loads(line)
            populate_bits(lines[i], stop_dict, arduino)

        stop_dicts.close()

        time.sleep(30)

    
