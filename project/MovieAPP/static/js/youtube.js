// HTML에서 정의된 전역 변수 movieTitle을 사용
console.log(`Movie Title (from JavaScript file): ${movieTitle}`);

function fetchTrailer(movieTitle) {
    const apiUrl = `/api/youtube-trailer?title=${encodeURIComponent(movieTitle)}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.videoId) {
                console.log(`"${movieTitle}" 예고편 ID: ${data.videoId}`);
                const videoPlayer = document.getElementById("videoPlayer");
                videoPlayer.src = `https://www.youtube.com/embed/${data.videoId}`;
            } else {
                console.error(`"${movieTitle}" 예고편을 찾을 수 없습니다.`);
            }
        })
        .catch(error => {
            console.error("YouTube 예고편 요청 실패:", error);
        });
}

window.onload = function () {
    if (movieTitle) {
        fetchTrailer(movieTitle);
    } else {
        console.error("영화 제목이 없습니다.");
    }
};
