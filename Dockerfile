FROM python:3.12-slim

# 환경 변수 설정
ENV DEBIAN_FRONTEND=noninteractive

# 필요한 리포지토리 추가 및 패키지 목록 업데이트
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository universe \
    && apt-get update

# 필요한 패키지 설치 (Java 및 Chromium 포함)
RUN apt-get install -y \
    curl \
    wget \
    unzip \
    chromium \
    chromium-driver \
    openjdk-11-jdk-headless \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정 (Selenium이 Chrome을 찾을 수 있도록)
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Java 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Gunicorn을 사용하여 Flask 애플리케이션 실행
CMD ["gunicorn", "-w", "2", "-k", "gevent", "portfolio:app", "--bind", "0.0.0.0:80", "--reload"]
