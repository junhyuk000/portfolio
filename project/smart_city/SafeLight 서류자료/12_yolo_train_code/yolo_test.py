import cv2
import os
import numpy as np
import torch
from ultralytics import YOLO

# YOLOv8 모델 로드 (네가 학습한 best.pt 사용)
model_path = r"C:\junhyuk\ALPR_data\plate\best.pt"
yolo_model = YOLO(model_path)

# 테스트할 이미지 파일 (한 개만)
test_image = r"C:\junhyuk\ALPR_data\car_image10.png"

# 결과 저장 폴더 설정
output_folder = r"C:\junhyuk\ALPR_data\dataset\Validation\output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 이미지 불러오기
img = cv2.imread(test_image)
if img is None:
    print(f"🚨 이미지 로드 실패: {test_image}")
else:
    # YOLOv8을 사용하여 번호판 탐지
    results = yolo_model(test_image, conf=0.1, imgsz=640)  # 신뢰도(conf) 조정 가능

    # 탐지된 객체에 대한 처리
    for result in results:
        for box in result.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box[:4])  # 바운딩 박스 좌표
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 박스 그리기
            cv2.putText(img, "Plate", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과 이미지 저장
    file_name = os.path.basename(test_image)
    save_path = os.path.join(output_folder, f"detected_{file_name}")
    cv2.imwrite(save_path, img)
    print(f"✅ 저장 완료: {save_path}")

print("\n🎯 테스트 완료! 탐지된 이미지는 output 폴더에 저장되었습니다.")
