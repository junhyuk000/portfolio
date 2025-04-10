// static/js/view_cctv.js

document.addEventListener('DOMContentLoaded', function() {
    // 현재 시간 표시
    function updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ko-KR', { 
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        });
        const dateString = now.toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
        
        const timestampEl = document.getElementById('current-time');
        if (timestampEl) {
            timestampEl.textContent = `${timeString}`;
        }
    }
    
    // 1초마다 시간 업데이트
    setInterval(updateCurrentTime, 1000);
    updateCurrentTime();
    
    // 센서 데이터 가져오기 - 임시로 비활성화하고 고정 데이터 사용
    function fetchSensorData() {
        /* API 호출 비활성화
        fetch('/api')
            .then(response => response.json())
            .then(data => {
                console.log("📩 받은 데이터:", data);
                
                // 카메라 용도 확인 (도로 or 인도)
                const purpose = document.querySelector('.info-list li:nth-child(2)').textContent;
                const isPurposeRoad = purpose.includes('도로');
                
                // ID 필터링
                let isValidData = false;
                if ((isPurposeRoad && data.ID == "1") || 
                    (!isPurposeRoad && data.ID == "2")) {
                    isValidData = true;
                }
                
                if (!isValidData) {
                    console.warn("⚠️ 해당 목적에 맞는 데이터가 없습니다.");
                    return;
                }
                
                // 안전 상태 업데이트
                const safetyStatus = document.getElementById("safety-status");
                if (safetyStatus) {
                    if (data["Switch State"] == "1") {
                        safetyStatus.innerHTML = `<i class="fas fa-shield-alt"></i> 현재 가로등 주변은 안전합니다.`;
                        safetyStatus.classList.remove('danger');
                    } else {
                        safetyStatus.innerHTML = `<i class="fas fa-exclamation-triangle"></i> 긴급 상황! SOS 버튼이 눌렸습니다!`;
                        safetyStatus.classList.add('danger');
                    }
                }
                
                // 온습도 정보 업데이트
                updateSensorReadings(data);
                
                // 가로등 상태 업데이트
                updateStreetlightStatus(data);
            })
            .catch(error => {
                console.error("데이터 불러오기 실패:", error);
            });
        */
        
        // 고정 데이터 사용 - 실제 API 연동 시 제거
        console.log("📊 고정 데이터 사용 중");
    }
    
    // 센서 측정값 업데이트
    function updateSensorReadings(data) {
        const temperatureReading = document.getElementById("temperature-reading");
        const humidityReading = document.getElementById("humidity-reading");
        const heatIndexReading = document.getElementById("heat-index-reading");
        
        if (temperatureReading && data.Temperature !== undefined) {
            temperatureReading.querySelector('span').textContent = `${data.Temperature}°C`;
        }
        
        if (humidityReading && data.Humidity !== undefined) {
            humidityReading.querySelector('span').textContent = `${data.Humidity}%`;
        }
        
        if (heatIndexReading && data["Heat Index"] !== undefined) {
            heatIndexReading.querySelector('span').textContent = `${data["Heat Index"]}°C`;
        }
    }
    
    // 가로등 상태 업데이트
    function updateStreetlightStatus(data) {
        const streetlightStatus = document.getElementById("streetlight-status");
        const statusIcon = streetlightStatus ? streetlightStatus.querySelector('.status-icon') : null;
        const statusText = streetlightStatus ? streetlightStatus.querySelector('span') : null;
        
        if (!streetlightStatus || !statusIcon || !statusText) return;
        
        if (data["LED State"] == "1") {
            statusIcon.classList.add('on');
            statusText.textContent = "가로등이 켜져 있습니다";
        } else {
            statusIcon.classList.remove('on');
            statusText.textContent = "가로등이 꺼져 있습니다";
        }
    }
    
    // 전체 화면 기능
    const fullscreenBtn = document.querySelector('.fullscreen-btn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', function() {
            const videoElement = document.getElementById('video-stream');
            
            if (!document.fullscreenElement) {
                if (videoElement.requestFullscreen) {
                    videoElement.requestFullscreen();
                } else if (videoElement.mozRequestFullScreen) {
                    videoElement.mozRequestFullScreen();
                } else if (videoElement.webkitRequestFullscreen) {
                    videoElement.webkitRequestFullscreen();
                } else if (videoElement.msRequestFullscreen) {
                    videoElement.msRequestFullscreen();
                }
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
            }
        });
    }
    
    // 스크린샷 기능
    const snapshotBtn = document.querySelector('.snapshot-btn');
    if (snapshotBtn) {
        snapshotBtn.addEventListener('click', function() {
            const videoElement = document.getElementById('video-stream');
            const streamContainer = document.querySelector('.cctv-stream-container');
            
            // 캔버스 생성 및 이미지 그리기
            const canvas = document.createElement('canvas');
            canvas.width = videoElement.naturalWidth || videoElement.width;
            canvas.height = videoElement.naturalHeight || videoElement.height;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            
            // 날짜와 시간 추가
            const now = new Date();
            const timestamp = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
            
            ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            ctx.fillRect(0, 0, canvas.width, 30);
            
            ctx.font = '14px Arial';
            ctx.fillStyle = 'white';
            ctx.fillText(timestamp, 10, 20);
            
            // 이미지 URL 생성
            const dataUrl = canvas.toDataURL('image/png');
            
            // 다운로드 링크 생성
            const link = document.createElement('a');
            link.href = dataUrl;
            link.download = `cctv_capture_${timestamp.replace(/[\s:-]/g, '_')}.png`;
            link.textContent = '스크린샷 다운로드';
            link.className = 'download-link';
            
            // 기존 다운로드 링크가 있으면 제거
            const existingLink = streamContainer.querySelector('.download-link');
            if (existingLink) {
                existingLink.remove();
            }
            
            // 다운로드 링크 추가
            streamContainer.appendChild(link);
        });
    }
    
    // 초기 데이터 로드만 실행 (고정 데이터 사용 중이므로 주기적 업데이트는 필요 없음)
    fetchSensorData();
});