#!/usr/bin/env python3.9

import requests
import time
import json
import os
#import serial
import time
import sys
import signal

import stops
import config
import constants

def populate_bits(line, stops, arduino, direction):
    out_bits = [0] * len(stops) #buffer of bits representing each stop
    
    VEHICLES_URL = "https://api-v3.mbta.com/vehicles?filter[route]=" + line + "&filter[direction_id]=" + direction + "&api_key=" + API_KEY
    vehicles = requests.get(url=VEHICLES_URL).json()['data'] # Get all vehicles on specified line and specified direction

    stop_ids = [str(v["relationships"]["stop"]["data"]["id"]) for v in vehicles] # Get stop IDs of all the vehicles

    STOPS_URL = f"https://api-v3.mbta.com/stops?filter[id]={','.join(stop_ids)}" + "&api_key=" + API_KEY
    stops_data = requests.get(url=STOPS_URL).json()['data'] # Use stop IDs to get all info of necessary stops

    # For each stop, get name and use dictionary of stops to change corresponding bit in buffer to 1
    for i in range(len(stops_data)): 
        stop_name = stops_data[i]['attributes']['name']
        out_bits[(stops[stop_name])] = 1

    binary_string = ''.join(map(str, out_bits)) # Write bits to string
    output = lineFlag[line] + binary_string + '\n' # Arduino output combining the flag of the line, the binary string, and a newline
    print(output)

    # Send the bytes serially
    #arduino.write(output.encode())

def main(direction):
    arduino = 1 #serial.Serial('/dev/ttyACM0', '9600')
    time.sleep(2)

    while True:
        stop_dicts.seek(0) # Reset file pointer to start
        for i, line in enumerate(stop_dicts):
            stop_dict = json.loads(line) # Load in stops dictionary
            populate_bits(lines[i], stop_dict, arduino, direction)

        time.sleep(2)

def parse_dir(dir):
    if dir.lower() == "n":
        return constants.NORTHBOUND
    elif dir.lower() == "s":
        return constants.SOUTHBOUND
    return -1

def signal_handler(sig, frame):
    print("\nClosing program")
    stop_dicts.close()
    sys.exit(0)

if __name__ == "__main__":
    arg_dir = sys.argv[1:]
    direction = parse_dir(arg_dir[0])

    if direction == -1:
        print("Not a valid direction code, either input n for northbound or s for southbound trains")
        exit(1)

    API_KEY = config.key

    lineFlag = {"Orange":"o", "Blue":"b", "Red":"r", "Green-B,Green-C,Green-D,Green-E":"g"}
    lines = ["Blue", "Orange", "Red", "Green-B,Green-C,Green-D,Green-E"]

    if not os.path.exists('stops.txt'):
        for line in lines:
            stops.populate_stop_dict(line)

    stop_dicts = open('stops.txt', 'r')

    signal.signal(signal.SIGINT, signal_handler)

    main(direction)

    
