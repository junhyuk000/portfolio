console.log("✅ map.js 로드됨!");
var mapContainer = document.getElementById('map');
var mapOption = {
    center: new kakao.maps.LatLng(36.5, 127.5), // 기본 중심 (대한민국)
    level: 13 // 확대 수준
};
var map = new kakao.maps.Map(mapContainer, mapOption);
var ps = new kakao.maps.services.Places();
var geocoder = new kakao.maps.services.Geocoder();
var map, ps, geocoder, markers = [];

// 🏁 맵 초기화 함수
function initializeMap() {
    console.log("📍 맵 초기화 실행");

    var mapContainer = document.getElementById('map');
    var mapOption = {
        center: new kakao.maps.LatLng(36.5, 127.5),
        level: 13
    };
    map = new kakao.maps.Map(mapContainer, mapOption);
    ps = new kakao.maps.services.Places();
    geocoder = new kakao.maps.services.Geocoder();

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            var currentPosition = new kakao.maps.LatLng(lat, lng);

            map.setCenter(currentPosition);
            map.setLevel(5);

            console.log("✅ 위치 정보 가져오기 성공:", lat, lng);
            searchCinemasAround(currentPosition);
        }, function (error) {
            console.error("🚨 위치 정보를 가져올 수 없음", error);
            alert("위치 정보를 가져올 수 없습니다. 기본 위치에서 검색합니다.");
            searchCinemasAround(mapOption.center);
        });
    } else {
        console.error("❌ Geolocation을 지원하지 않습니다.");
        alert("위치 정보 사용이 불가능합니다.");
        searchCinemasAround(mapOption.center);
    }
}
// 🔍 키워드 기반 영화관 검색
function searchCinemasAround(centerLatLng) {
    var keywords = ['롯데시네마', '메가박스', 'CGV'];
    var allResults = [];
    removeMarkers();

    keywords.forEach(function (keyword, index) {
        ps.keywordSearch(keyword, function (data, status, pagination) {
            if (status === kakao.maps.services.Status.OK) {
                allResults = allResults.concat(data);
                console.log(`"${keyword}" 검색 성공:`, data);

                if (index === keywords.length - 1 && !pagination.hasNextPage) {
                    displayResults(allResults);
                }

                if (pagination.hasNextPage) {
                    getNextPage(pagination, allResults, index, keywords.length - 1);
                }
            } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
                console.log(`"${keyword}" 검색 결과 없음`);
            } else {
                console.error(`"${keyword}" 검색 중 오류 발생`);
            }
        }, { location: centerLatLng, radius: 5000 });
    });
}

// 🎯 페이지네이션으로 추가 데이터 가져오기
function getNextPage(pagination, allResults, currentIndex, lastIndex) {
    pagination.nextPage();
    pagination.callback = function (data, status, nextPagination) {
        if (status === kakao.maps.services.Status.OK) {
            allResults = allResults.concat(data);
            console.log('추가 페이지 검색 성공:', data);

            if (currentIndex === lastIndex && !nextPagination.hasNextPage) {
                displayResults(allResults);
            }

            if (nextPagination.hasNextPage) {
                getNextPage(nextPagination, allResults, currentIndex, lastIndex);
            }
        } else {
            console.error('추가 페이지 검색 중 오류:', status);
        }
    };
}

// 🏷️ 검색 결과 표시 및 리스트 추가
function displayResults(results) {
    var listEl = document.getElementById('placesList');
    var bounds = new kakao.maps.LatLngBounds();
    listEl.innerHTML = '';

    results.forEach(function (result) {
        var position = new kakao.maps.LatLng(result.y, result.x);
        var marker = new kakao.maps.Marker({ position: position });
        marker.setMap(map);
        markers.push(marker);

        var listItem = document.createElement('li');
        listItem.innerHTML = `<b>${result.place_name}</b> (${result.address_name})`;
        listItem.dataset.lat = result.y;
        listItem.dataset.lng = result.x;
        listEl.appendChild(listItem);

        listItem.addEventListener('click', function () {
            map.setCenter(new kakao.maps.LatLng(this.dataset.lat, this.dataset.lng));
            map.setLevel(3);
        });

        bounds.extend(position);
    });

    map.setBounds(bounds);
}

// 📍 주소 검색 기능
function searchByAddress() {
    var address = document.getElementById('searchInput').value.trim();

    if (!address) {
        alert('주소를 입력해주세요.');
        return;
    }

    geocoder.addressSearch(address, function (result, status) {
        if (status === kakao.maps.services.Status.OK) {
            var centerLatLng = new kakao.maps.LatLng(result[0].y, result[0].x);
            map.setCenter(centerLatLng);
            map.setLevel(5);
            console.log(`주소 검색 성공: ${address}`, result);

            searchCinemasAround(centerLatLng);
        } else {
            alert('주소 검색 결과가 없습니다.');
        }
    });
}

// 기존 마커 제거
function removeMarkers() {
    markers.forEach(function (marker) {
        marker.setMap(null);
    });
    markers = [];
}

// 검색 버튼 이벤트 리스너
document.getElementById('searchButton').addEventListener('click', function () {
    console.log('주소 검색 버튼 클릭됨');
    searchByAddress();
});

// 🌍 지도 초기화 및 자동 검색 실행
initializeMap();