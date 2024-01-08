# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, Response, redirect, url_for
import requests
import subprocess
import sys

# Import custom modules
from preset import Preset
from camera import Camera

# Initialize Flask application
app = Flask(__name__)

# Initialize global variables
process = None
script_running = False
rtsp_url = 'your_rtsp_stream_url'
latest_frame = None

# Initialize Camera and Preset modules
camera = Camera(rtsp_url)
preset = Preset('preset.txt')

# Function to generate frames from the camera
def gen_frames():
    while True:
        frame = camera.get_latest_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Define route for the main page of the web application
@app.route('/', methods=['GET', 'POST'])
def index():
    global process, script_running
    status = 'Ziadny'
    presets = ['']
    sleep_times = ['']

    # Read presets and sleep times from file
    with open('preset.txt', 'a+') as f:
        f.seek(0)  # Move the read cursor to the start of the file
        lines = f.read().splitlines()
        presets = lines[::2]  # Get the presets (every other line starting from the first line)
        sleep_times = lines[1::2]  # Get the sleep times (every other line starting from the second line)

    # Read status from file
    with open('status.txt', 'a+') as f:
        f.seek(0)  # Move the read cursor to the start of the file
        status = f.read().strip()

    # Handle POST requests (buttons in index)
    if request.method == 'POST':
        if 'save' in request.form:
            # Save presets and sleep times to file
            # Extract all the values from the form where the key starts with 'preset'.
            presets = [value for key, value in request.form.items() if key.startswith('preset')] 
            # Extract all the values from the form where the key starts with 'sleep_time'.
            sleep_times = [value for key, value in request.form.items() if key.startswith('sleep_time')]
            with open('preset.txt', 'w') as f:
                for preset, sleep_time in zip(presets, sleep_times):
                    f.write(f'{preset}\n{sleep_time}\n')

        elif 'load' in request.form:
            # Load presets and sleep times from file
            try:
                with open('preset.txt', 'r') as f:
                    lines = f.read().splitlines()
                    presets = lines[::2]  # Get the presets (every other line starting from the first line)
                    sleep_times = lines[1::2]  # Get the sleep times (every other line starting from the second line)
            except FileNotFoundError:
                # If not found continue with empty form
                pass

        elif 'start' in request.form and process is None:
            # If the 'start' button is pressed and no process is currently running,
            # start a new subprocess running the 'loop.py' script
            process = subprocess.Popen([sys.executable, 'loop.py'])
            script_running = True

        elif 'stop' in request.form and process is not None:
            # If the 'stop' button is pressed and a process is currently running,
            # terminate the process
            process.terminate()
            process = None
            script_running = False

    if script_running:
         # If a script is running, read the status from the 'status.txt' file
        with open('status.txt', 'r') as f:
            status = f.read()
    
    # Render the 'index.html' template with the current status, presets, and sleep times
    return render_template('index.html', script_running=script_running, status=status, presets=presets, sleep_times=sleep_times)

@app.route('/status', methods=['GET'])
def status():
    # Define a route for getting the current status, if script is not running write 'None'
    status = 'Ziadny'
    if script_running:
        # If a script is running, read the status from the 'status.txt' file
        with open('status.txt', 'r') as f:
            status = f.read()
    return status

@app.route('/video_feed')
def video_feed():
    # Define a route for getting the video feed
    # The 'gen_frames' function is used to generate the frames for the video feed
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/delete_last', methods=['POST'])
def delete_last():
    # Define a route for deleting the last preset
    # Initialize a Preset object with the 'preset.txt' file
    preset = Preset('preset.txt')
    # Call the delete_last method of the Preset object to delete the last preset and sleep_time
    preset.delete_last()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # If this script is run directly (not imported as a module), then start the Flask application
    app.run(host='0.0.0.0', port=80)

