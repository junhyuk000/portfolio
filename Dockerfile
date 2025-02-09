FROM python:3.12-slim

# 환경 변수 설정
ENV DEBIAN_FRONTEND=noninteractive

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    chromium \
    chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정 (Selenium이 Chrome을 찾을 수 있도록)
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Gunicorn을 사용하여 Flask 애플리케이션 실행
CMD ["gunicorn", "-w", "2", "-k", "gevent", "portfolio:app", "--bind", "0.0.0.0:8080", "--reload"]
