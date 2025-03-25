import requests
import time
import json
import os
import serial
import time

import stops
import config
import constants
import sys

API_KEY = config.key

lineFlag = {"Orange":"o", "Blue":"b", "Red":"r", "Green":"g"}
lines = ["Blue", "Orange", "Red"]

def populate_bits(line, stops, arduino, direction):
    out_bits = [0] * len(stops)
    
    VEHICLES_URL = "https://api-v3.mbta.com/vehicles?filter[route]=" + line + "&filter[direction_id]=" + direction
    vehicles = requests.get(url=VEHICLES_URL).json()['data']

    stop_ids = [str(v["relationships"]["stop"]["data"]["id"]) for v in vehicles]

    STOPS_URL = f"https://api-v3.mbta.com/stops?filter[id]={','.join(stop_ids)}"
    stops_data = requests.get(url=STOPS_URL).json()

    for i in range(len(vehicles)):
        stop_name = stops_data['data'][i]['attributes']['name']

        out_bits[(stops[stop_name])] = 1

    binary_string = ''.join(map(str, out_bits))
    output = lineFlag[line] + binary_string + '\n'
    print(output)

    # Send the bytes serially
    arduino.write(output.encode())

def main(direction):
    arduino = serial.Serial('/dev/ttyACM0', '9600')
    time.sleep(2)

    if not os.path.exists('stops.txt'):
        stops.populate_stop_dict()

    while True:
        stop_dicts = open('stops.txt', 'r')

        for i, line in enumerate(stop_dicts):
            stop_dict = json.loads(line)
            populate_bits(lines[i], stop_dict, arduino, direction)
            time.sleep(1)

        stop_dicts.close()

        time.sleep(30)

def parse_dir(dir):
    if dir.lower() == "n":
        return constants.NORTHBOUND
    elif dir.lower() == "s":
        return constants.SOUTHBOUND
    return -1


if __name__ == "__main__":
    arg_dir = sys.argv[1:]
    direction = parse_dir(arg_dir[0])

    if direction == -1:
        print("Not a valid direction code, either input n for northbound or s for southbound trains")
        exit(1)

    main(direction)

    
