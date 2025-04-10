from flask import Flask, request, render_template
from datetime import datetime
import os

app = Flask(__name__)

# 메모리에 저장 (DB 없이)
sos_alerts = []

@app.route("/sos_alert", methods=["POST"])
def receive_sos_alert():
    data = request.json
    print("🚨 SOS 수신:", data)

    sos_alerts.append({
        "location": data.get("location"),
        "stream_url": data.get("stream_url"),
        "timestamp": data.get("timestamp"),
        "type": data.get("type", "SOS")
    })

    return "✅ SOS 수신 완료", 200

@app.route("/sos_data")
def sos_data():
    return {"alerts": sos_alerts}


@app.route("/")
def sos_dashboard():
    return render_template("sos_dashboard.html", alerts=sos_alerts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
