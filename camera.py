import cv2
import threading

class Camera:
    def __init__(self, rtsp_url):
        self.cap = cv2.VideoCapture(rtsp_url)
        self.latest_frame = None
        self.capture_thread = threading.Thread(target=self.capture_frames)
        self.capture_thread.start()

    def capture_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                self.latest_frame = buffer.tobytes()

    def get_latest_frame(self):
        return self.latest_frame