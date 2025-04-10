from flask import request, jsonify

# 전역 변수로 데이터 저장
received_data = {"message": "No data received"}

def handle_request():
    """POST 또는 GET 요청을 처리하는 함수"""
    global received_data

    if request.method == "POST":
        if request.is_json:
            received_data = request.get_json()
            return jsonify({"status": "success", "message": "JSON data received", "data": received_data})

        if not request.form:
            return jsonify({"status": "error", "message": "No data received"}), 400

        raw_data_list = list(request.form.keys())
        if not raw_data_list:
            return jsonify({"status": "error", "message": "Empty form data"}), 400

        raw_data = raw_data_list[0]
        data_dict = {}

        pairs = raw_data.split("|")
        for pair in pairs:
            key_value = pair.strip().split(":")
            if len(key_value) == 2:
                key, value = key_value[0].strip(), key_value[1].strip()
                data_dict[key] = value

        received_data = data_dict
        print(f"📩 변환된 데이터: {received_data}")  # 터미널에서 확인

        return received_data

    return received_data  # GET 요청 시 최신 데이터 반환