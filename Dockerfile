FROM python:3.12-slim

# 환경 변수 설정
ENV DEBIAN_FRONTEND=noninteractive

# 저장소 업데이트 및 OpenJDK 저장소 활성화
RUN echo "deb http://deb.debian.org/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    apt-get update

# 필수 패키지 설치
RUN apt-get install -y \
    curl \
    wget \
    unzip \
    apt-transport-https \
    ca-certificates \
    gnupg \
    chromium \
    chromium-driver \
    default-jdk \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정 (Selenium이 Chrome을 찾을 수 있도록)
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Java 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# ✅ `gevent`와 `gunicorn`을 먼저 설치
RUN pip install --no-cache-dir gevent gunicorn

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Gunicorn을 사용하여 Flask 애플리케이션 실행
CMD ["gunicorn", "-w", "1", "-k", "gevent", "portfolio:app", "--bind", "0.0.0.0:80", "--preload"]
