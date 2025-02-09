// HTML에서 정의된 전역 변수 movieTitle을 사용
console.log(`Movie Title (from JavaScript file): ${movieTitle}`);

// 유튜브 API 호출
function fetchTrailer(movieTitle) {
    const query = `${movieTitle.trim()} 예고편`;
    const searchUrl = "https://www.googleapis.com/youtube/v3/search";
    const apiKey = "AIzaSyCStt6OCKJD2YY1wOPVkR88PZMjknY3EPw"; // 유튜브 API 키

    const url = `${searchUrl}?part=snippet&q=${encodeURIComponent(query)}&type=video&key=${apiKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.items && data.items.length > 0) {
                const videoId = data.items[0].id.videoId;
                console.log(`"${movieTitle}" 예고편 ID: ${videoId}`);

                // 유튜브 플레이어 업데이트
                const videoPlayer = document.getElementById("videoPlayer");
                videoPlayer.src = `https://www.youtube.com/embed/${videoId}`;
            } else {
                console.error(`"${movieTitle}" 예고편을 찾을 수 없습니다.`);
            }
        })
        .catch(error => console.error("유튜브 API 요청 오류:", error));
}

// 페이지 로드 시 실행
window.onload = function() {
    if (movieTitle) {
        fetchTrailer(movieTitle);
    } else {
        console.error("영화 제목이 없습니다.");
    }
};
