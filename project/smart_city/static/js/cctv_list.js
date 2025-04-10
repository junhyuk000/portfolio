// static/js/cctv_list.js

document.addEventListener('DOMContentLoaded', function() {
    // 검색창 자동 포커스 (빈 경우에만)
    const searchInput = document.getElementById('search_query');
    if (searchInput && searchInput.value === '') {
        setTimeout(() => searchInput.focus(), 500);
    }
    
    // 검색 타입에 따른 플레이스홀더 변경
    const searchType = document.getElementById('search_type');
    if (searchType) {
        searchType.addEventListener('change', updatePlaceholder);
        // 초기 로딩 시 한 번 업데이트
        updatePlaceholder();
    }
    
    // 테이블 행에 호버 효과
    const dataRows = document.querySelectorAll('.data-row');
    dataRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--table-row-hover');
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // 미설치 버튼 클릭 시 알림
    const disabledButtons = document.querySelectorAll('.view-button.disabled');
    disabledButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            showNotification('이 가로등에는 CCTV가 설치되어 있지 않습니다.', 'warning');
        });
    });
    
    // 검색 폼 제출 시 유효성 검사
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            if (searchType.value !== 'all' && searchInput.value.trim() === '') {
                e.preventDefault();
                showNotification('검색어를 입력해주세요.', 'warning');
                searchInput.focus();
            }
        });
    }
    
    // 검색어 입력 시 엔터키 제출
    if (searchInput) {
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchForm.dispatchEvent(new Event('submit'));
            }
        });
    }
});

// 검색 타입에 따른 플레이스홀더 업데이트
function updatePlaceholder() {
    const searchType = document.getElementById('search_type');
    const searchInput = document.getElementById('search_query');
    
    if (!searchType || !searchInput) return;
    
    switch (searchType.value) {
        case 'street_light_id':
            searchInput.placeholder = '가로등 번호를 입력하세요';
            break;
        case 'street_light_location':
            searchInput.placeholder = '위치를 입력하세요';
            break;
        case 'all':
            searchInput.placeholder = '검색어를 입력하세요';
            break;
        default:
            searchInput.placeholder = '검색어를 입력하세요';
    }
}

// 알림 표시 함수
function showNotification(message, type = 'info') {
    const notificationContainer = document.createElement('div');
    notificationContainer.className = `flash-message ${type}`;
    notificationContainer.textContent = message;
    
    document.body.appendChild(notificationContainer);
    
    // 페이드 인 효과
    setTimeout(() => {
        notificationContainer.classList.add('show');
    }, 10);
    
    // 5초 후 제거
    setTimeout(() => {
        notificationContainer.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notificationContainer);
        }, 300);
    }, 5000);
}