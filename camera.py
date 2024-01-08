# Import necessary modules
import cv2
import threading

class Camera:
    def __init__(self, rtsp_url):
        # Initialize the Camera object with a RTSP URL
        # Create a VideoCapture object for the RTSP URL
        self.cap = cv2.VideoCapture(rtsp_url)
        self.latest_frame = None
        # Start a new thread that will capture frames from the video stream
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.start()

    def capture_frames(self):
         # Continuously capture frames from the video stream
        while True:
            # Read the next frame from the video stream
            success, frame = self.cap.read()
            if not success:
                # If the frame could not be read, break the loop
                break
            else:
                # If the frame was read successfully, encode it as a JPEG image
                ret, buffer = cv2.imencode('.jpg', frame)
                # Convert the JPEG image to bytes and store it as the latest frame
                self.latest_frame = buffer.tobytes()

    def get_latest_frame(self):
        # Return the latest frame captured from the video stream
        return self.latest_frame