
# CamLoop-Web

Automatic camera rotation using IP Camera CGI API position preset calling via http requests

## Clone the repo

```bash
git clone https://github.com/WitcherTro/Camloop-Web.git

```

## Dependencies
This project needs these dependencies to function properly:
- Flask
- Requests
- OpenCV-python

To download them into your enviroment you can use pip:
```bash
pip install flask requests opencv-python
```

## Setting up camera
Inside loop.py you change ip address to your camera WebUi with authentification

```python
CAMURL = 'http://user:password@camera_ip_address'
```
example:
```python
CAMURL = 'http://admin:Pass123@192.168.1.10'
```

  
If your camera supports RTSP stream then also change url in main.py
```python
rtsp_url = 'your_rtsp_stream_url'
```
example:
```python
rtsp_url = 'rtsp://192.168.1.10:554/11'
```
## Running application and setting specific port

To set custom port on which application will run, change port number in main.py:
```python
app.run(host='0.0.0.0', port=80)
```

  
to run the application, simply start main.py in terminal
```bash
(cd to cloned repo)
$ python main.py
```
## Using application
to connect to your application, inside your browser type localhost or 127.0.0.1 (by default port is set to 80), 
if you set custom port you may need to specify port too as ip:port 

after connecting you should see control panel on the left and camera stream on the right

Control panel has these functions:  

  
**Start CamLoop**   
Starts the camera loop with specified presets and time sleeps  

  
**Stop CamLoop**  
Stops the camera loop


**Preset and time sleep table**  
| Preset | Time sleep (s) |
| :------: | :--------------: |
|   index of called preset    | time how long should camera stay in the preset       |
| 1 | 60 |
| 2 | 15 |

**Table buttons**  

**-Add new row**  
**Remove last row**  
**Save**  
**Load**  

**Text indicator if CamLoop is running and on what preset it currently is**
