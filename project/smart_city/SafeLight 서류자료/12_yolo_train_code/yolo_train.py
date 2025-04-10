from ultralytics import YOLO

def train_yolov8():
    """ YOLOv8을 사용한 번호판 추가 학습 코드 """
    model = YOLO("yolov8n.pt")  # 사전 학습된 YOLOv8n 모델 로드

    model.train(
        data=r"C:\junhyuk\ALPR_data\numplate_segmentation.v5i.yolov8-obb\data.yaml",  # 데이터셋 설정
        epochs=50,       # 🚀 50 Epoch 학습
        patience=10,     # 조기 종료 활성화 (10 epoch 동안 개선 없으면 중지)
        imgsz=640,       # 이미지 크기
        batch=16,        # 배치 크기
        device="cuda",   # GPU 사용
        workers=0,       # Windows에서 multiprocessing 문제 방지
        mosaic=1.0,      # 모자이크 데이터 증강 활성화
        flipud=0.5,      # 상하 반전
        fliplr=0.5,      # 좌우 반전
        scale=0.5,       # 크기 조절
        translate=0.1    # 이동 변환
    )

    print("✅ 번호판 추가된 YOLO 학습이 완료되었습니다.")

if __name__ == "__main__":
    train_yolov8()
