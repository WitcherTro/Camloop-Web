import requests, time


CAMURL = 'http://meno:heslo@192.168.2.143'
REQUEST = '/web/cgi-bin/hi3510/param.cgi?cmd=preset&-act=goto&-status=1&-number='
CAMREQ = CAMURL + REQUEST

while True:
    for i in range(4):
        response = requests.get(CAMREQ + str(i))
        with open('status.txt', 'w') as f:
            f.write(str(i+1))
        time.sleep(20)

