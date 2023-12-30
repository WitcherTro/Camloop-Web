from flask import Flask, render_template, request, Response
import requests
import subprocess
import sys
import cv2
import threading

app = Flask(__name__)
process = None
script_running = False
rtsp_url = 'rtsp://meno:heslo@192.168.2.143:554/11'
latest_frame = None

cap = cv2.VideoCapture(rtsp_url)

def capture_frames():
    global latest_frame
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            latest_frame = buffer.tobytes()

capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

def gen_frames():
    while True:
        if latest_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')



@app.route('/', methods=['GET', 'POST'])
def index():
    global process, script_running
    status = 'ziadny'
    if request.method == 'POST':
        if 'start' in request.form:
            process = subprocess.Popen([sys.executable, 'loop.py'])
            script_running = True
        elif 'stop' in request.form and process is not None:
            process.terminate()
            process = None
            script_running = False
    if script_running:
        with open('status.txt', 'r') as f:
            status = f.read()
    return render_template('index.html', script_running=script_running, status=status)

@app.route('/status', methods=['GET'])
def status():
    status = 'ziadny'
    if script_running:
        with open('status.txt', 'r') as f:
            status = f.read()
    return status

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

