from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime

app = Flask(__name__)

# 감지된 차량 데이터 저장용
detected_vehicles = []

# 폴더 생성 (이미지 저장 경로가 있다면)
os.makedirs("static/received_images", exist_ok=True)

@app.route('/receive_alert', methods=['POST'])
def receive_alert():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    print(f"🚨 감지된 차량 정보 수신: {data}")

    detected_vehicles.append({
        "license_plate": data.get("license_plate"),
        "image_path": data.get("image_path"),  # 이미지 URL
        "timestamp": data.get("timestamp"),
        "camera_location": data.get("camera_location"),
        "stream_url": data.get("stream_url")
    })

    return jsonify({"status": "received"}), 200

@app.route('/', methods=['GET'])
def view_alerts():
    return render_template('index.html', vehicles=detected_vehicles)


# 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)