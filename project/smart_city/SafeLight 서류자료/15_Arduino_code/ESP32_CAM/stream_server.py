import cv2
import threading
import requests
import numpy as np
from flask import Flask, Response

ESP32_CAM_URL = "http://10.0.66.18:80"  # ✅ ESP32-CAM의 IP 주소
app = Flask(__name__)

# 비디오 프레임 버퍼
frame = None
lock = threading.Lock()

def capture_stream():
    global frame
    while True:
        try:
            response = requests.get(ESP32_CAM_URL, stream=True, timeout=5)
            bytes_data = b""
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    bytes_data = bytes_data[b+2:]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if img is not None:
                        with lock:
                            frame = img
        except Exception as e:
            print(f"⚠️ 스트리밍 오류: {e}")

# Flask에서 MJPEG 스트리밍을 제공하는 함수
def generate():
    global frame
    while True:
        with lock:
            if frame is None:
                continue
            _, jpeg = cv2.imencode('.jpg', frame)
            if not _:
                continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/stream')
def stream():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    threading.Thread(target=capture_stream, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
