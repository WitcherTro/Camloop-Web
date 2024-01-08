# Import necessary modules
import requests, time

# Define the base URL for the camera and the request string
CAMURL = 'http://meno:heslo@192.168.2.143'
REQUEST = '/web/cgi-bin/hi3510/param.cgi?cmd=preset&-act=goto&-status=1&-number='
CAMREQ = CAMURL + REQUEST

try:
     # Try to open the 'preset.txt' file and read the presets and sleep times
    with open('preset.txt', 'r') as f:
        lines = f.read().splitlines()
        presets = lines[::2]  
        sleep_times = [int(time) for time in lines[1::2]]  
except FileNotFoundError:
    # If the 'preset.txt' file does not exist, initialize empty lists for presets and sleep times
    presets = []
    sleep_times = []

while True:
    # Loop indefinitely
    for preset, sleep_time in zip(presets, sleep_times):
        # For each preset and corresponding sleep time, send a request to the camera to go to the preset
        response = requests.get(CAMREQ + preset)
        # Write the current preset to the 'status.txt' file
        with open('status.txt', 'w') as f:
            f.write(preset)
        # Sleep for the specified amount of time before moving to the next preset
        time.sleep(sleep_time)