import cv2
import numpy as np
import threading
import base64
import time
import os
import requests
from datetime import datetime
from ultralytics import YOLO
import re

# ====================== 📌 전역 변수 ======================
VIDEO_STREAM_URL = None  # ← 동적으로 세팅
camera_location = "위치 정보 없음"
camera_stream_url = None

# YOLO 모델 로드 (번호판 검출)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.pt")
model = YOLO(MODEL_PATH)

# Google Cloud OCR API 설정
VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"
API_KEY = os.getenv("GOOGLE_API_KEY")

ocr_result = ""
plate_counts = {}
ALERT_THRESHOLD = 5
OCR_INTERVAL = 3.0
saved_plates = set()
alert_message = ""

frame = None
lock = threading.Lock()

# ====================== 📌 설정 함수 ======================
def set_camera_info(location, stream_url):
    """app.py에서 카메라 위치 및 URL을 전달받아 설정"""
    global camera_location, camera_stream_url, VIDEO_STREAM_URL
    camera_location = location
    camera_stream_url = stream_url
    VIDEO_STREAM_URL = stream_url
    print(f"✅ 카메라 설정 완료 - 위치: {camera_location}, URL: {camera_stream_url}")

# ====================== 📷 스트리밍 ======================
def fetch_stream():
    global frame
    while VIDEO_STREAM_URL is None:
        time.sleep(0.1)  # 설정되기 전까지 대기

    cap = cv2.VideoCapture(VIDEO_STREAM_URL)
    while True:
        ret, img = cap.read()
        if not ret:
            continue
        with lock:
            frame = img

# ====================== 🔍 번호판 검출 ======================
def detect_license_plate():
    global ocr_result, plate_counts, alert_message
    while True:
        time.sleep(OCR_INTERVAL)
        with lock:
            if frame is None:
                continue
            img = frame.copy()

        results = model(img)
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                plate_img = img[y1:y2, x1:x2]
                if plate_img.size > 0:
                    plate_text = run_ocr(plate_img)
                    if plate_text:
                        plate_counts[plate_text] = plate_counts.get(plate_text, 0) + 1
                        if plate_counts[plate_text] >= ALERT_THRESHOLD and plate_text not in saved_plates:
                            save_detected_plate(plate_text, img)

# ====================== 🧠 OCR ======================
def run_ocr(plate_img):
    global ocr_result
    _, buffer = cv2.imencode(".jpg", plate_img)
    base64_image = base64.b64encode(buffer).decode("utf-8")

    request_data = {
        "requests": [{
            "image": {"content": base64_image},
            "features": [{"type": "TEXT_DETECTION"}],
            "imageContext": {"languageHints": ["ko"]}
        }]
    }

    response = requests.post(f"{VISION_API_URL}?key={API_KEY}", json=request_data)
    if response.status_code == 200:
        result = response.json()
        texts = result["responses"][0].get("textAnnotations", [])
        if texts:
            raw_text = texts[0]["description"].strip()
            plate_text = clean_license_plate_text(raw_text)
            ocr_result = plate_text
            return plate_text
    print("❌ OCR 실패")
    return ""

def clean_license_plate_text(text):
    text = re.sub(r"[^가-힣0-9]", "", text)
    if len(text) == 7 and text[2].isalpha():
        return text
    elif len(text) == 8 and text[3].isalpha():
        return text
    elif len(text) == 9 and text[0].isalpha() and text[1].isalpha() and text[4].isalpha():
        return text
    return ""

# ====================== 💾 저장 및 전송 ======================
def save_detected_plate(plate_text, full_image):
    global alert_message
    if plate_text in saved_plates:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{plate_text}_{timestamp}.jpg"
    save_path = os.path.join("static/car_images", filename)
    cv2.imwrite(save_path, full_image)
    saved_plates.add(plate_text)

    alert_message = f"🚨 {plate_text} 불법 주정차 차량 발견!"
    print(f"📁 이미지 저장 완료: {save_path}")

    send_alert_to_police(plate_text, save_path)

def send_alert_to_police(plate_text, image_path):
    POLICE_SERVER_URL = "http://10.0.66.89:5002/receive_alert"
    data = {
        "license_plate": plate_text,
        "image_path": f"http://10.0.66.94:5010/static/car_images/{os.path.basename(image_path)}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "camera_location": camera_location,
        "stream_url": camera_stream_url
    }

    try:
        response = requests.post(POLICE_SERVER_URL, json=data)
        if response.status_code == 200:
            print(f"✅ 경찰서 서버 응답: {response.status_code}, {response.text}")
        else:
            print(f"❌ 경찰서 서버 응답 오류: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ 경찰서 서버 전송 오류: {e}")

# ====================== ▶️ 백그라운드 스레드 실행 ======================
threading.Thread(target=fetch_stream, daemon=True).start()
threading.Thread(target=detect_license_plate, daemon=True).start()
