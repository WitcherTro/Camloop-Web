from flask import Flask, render_template, request, Response, redirect, url_for
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
    presets = ['']
    sleep_times = ['']

    with open('preset.txt', 'a+') as f:
        f.seek(0)  # Move the read cursor to the start of the file
        lines = f.read().splitlines()
        presets = lines[::2]  # Get the presets (every other line starting from the first line)
        sleep_times = lines[1::2]  # Get the sleep times (every other line starting from the second line)

    with open('status.txt', 'a+') as f:
        f.seek(0)  # Move the read cursor to the start of the file
        status = f.read().strip()

    if request.method == 'POST':
        if 'save' in request.form:
            presets = [value for key, value in request.form.items() if key.startswith('preset')]
            sleep_times = [value for key, value in request.form.items() if key.startswith('sleep_time')]
            with open('preset.txt', 'w') as f:
                for preset, sleep_time in zip(presets, sleep_times):
                    f.write(f'{preset}\n{sleep_time}\n')

        elif 'load' in request.form:
            try:
                with open('preset.txt', 'r') as f:
                    lines = f.read().splitlines()
                    presets = lines[::2]  # Get the presets (every other line starting from the first line)
                    sleep_times = lines[1::2]  # Get the sleep times (every other line starting from the second line)
            except FileNotFoundError:
                pass

        elif 'start' in request.form:
            process = subprocess.Popen([sys.executable, 'loop.py'])
            script_running = True

        elif 'stop' in request.form and process is not None:
            process.terminate()
            process = None
            script_running = False

    if script_running:
        with open('status.txt', 'r') as f:
            status = f.read()
    return render_template('index.html', script_running=script_running, status=status, presets=presets, sleep_times=sleep_times)

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

@app.route('/delete_last', methods=['POST'])
def delete_last():
    with open('preset.txt', 'r') as f:
        lines = f.read().splitlines()

    # Check if there are at least two lines to delete (a preset and a sleep time)
    if len(lines) >= 2:
        # Delete the last two lines (the last preset and sleep time)
        lines = lines[:-2]

        with open('preset.txt', 'w') as f:
            for line in lines:
                f.write(f'{line}\n')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

