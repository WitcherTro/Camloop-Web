import requests, time


CAMURL = 'http://meno:heslo@192.168.2.143'
REQUEST = '/web/cgi-bin/hi3510/param.cgi?cmd=preset&-act=goto&-status=1&-number='
CAMREQ = CAMURL + REQUEST

try:
    with open('preset.txt', 'r') as f:
        lines = f.read().splitlines()
        presets = lines[::2]  
        sleep_times = [int(time) for time in lines[1::2]]  
except FileNotFoundError:
    presets = []
    sleep_times = []

while True:
    for preset, sleep_time in zip(presets, sleep_times):
        response = requests.get(CAMREQ + preset)
        with open('status.txt', 'w') as f:
            f.write(preset)
        time.sleep(sleep_time)