document.addEventListener('DOMContentLoaded', function() {
    // 현재 로그인한 관리자 ID 가져오기 (Flask 서버에서 제공되는 정보)
    const adminIdMeta = document.querySelector('meta[name="admin_id"]');
    const adminId = adminIdMeta ? adminIdMeta.getAttribute('content') : null; // adminId 변수 선언
    
    console.log('Current admin ID:', adminId); // 디버깅용
    
    // 사용자별 고유 키 생성
    const storageKey = `adminFavorites_${adminId}`;
    
    // 로컬 스토리지에서 즐겨찾기 가져오기 (사용자별)
    const favorites = JSON.parse(localStorage.getItem(storageKey)) || [];
    
    // 즐겨찾기 별 초기화
    const stars = document.querySelectorAll('.favorite-star');
    stars.forEach(star => {
        const title = star.getAttribute('data-title');
        const url = star.getAttribute('data-url');
        
        // URL을 기준으로 즐겨찾기 확인 (제목 대신)
        if (favorites.some(fav => fav.url === url)) {
            star.classList.add('active');
        }
        
        // 클릭 이벤트 추가
        star.addEventListener('click', function(e) {
            e.preventDefault();
            toggleFavorite(title, url, star, adminId);
        });
    });
    
    // 즐겨찾기 네비게이션 업데이트
    updateFavoritesNav(adminId);
    
    // 기존 데이터 마이그레이션 (한 번만 실행)
    migrateOldFavorites(adminId);
});

// 즐겨찾기 토글 함수
function toggleFavorite(title, url, starElement, adminId) {
    const storageKey = `adminFavorites_${adminId}`;
    const favorites = JSON.parse(localStorage.getItem(storageKey)) || [];
    
    // URL을 기준으로 즐겨찾기 확인
    const index = favorites.findIndex(fav => fav.url === url);
    
    if (index === -1) {
        // 즐겨찾기 추가
        favorites.push({ title, url });
        starElement.classList.add('active');
    } else {
        // 즐겨찾기 제거
        favorites.splice(index, 1);
        starElement.classList.remove('active');
    }
    
    // 로컬 스토리지에 저장 (사용자별)
    localStorage.setItem(storageKey, JSON.stringify(favorites));
    
    // 즐겨찾기 네비게이션 업데이트
    updateFavoritesNav(adminId);
}

// 즐겨찾기 네비게이션 업데이트
function updateFavoritesNav(adminId) {
    const storageKey = `adminFavorites_${adminId}`;
    const favorites = JSON.parse(localStorage.getItem(storageKey)) || [];
    const favoritesNav = document.getElementById('favorites-nav');
    const noFavoritesMessage = document.getElementById('no-favorites-message');
    
    if (!favoritesNav || !noFavoritesMessage) return; // 요소가 없으면 함수 종료
    
    // 기존 즐겨찾기 링크 제거 (라벨은 유지)
    const links = favoritesNav.querySelectorAll('a.nav-link');
    links.forEach(link => link.remove());
    
    // 즐겨찾기 없음 메시지 처리
    if (favorites.length === 0) {
        noFavoritesMessage.style.display = 'inline';
    } else {
        noFavoritesMessage.style.display = 'none';
        
        // 즐겨찾기 링크 추가
        favorites.forEach(fav => {
            const link = document.createElement('a');
            link.href = '#';
            link.className = 'nav-link';
            link.textContent = fav.title;
        
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const fullUrl = window.location.origin + fav.url;
                window.location.href = fullUrl;
            });
        
            favoritesNav.appendChild(link);
        });
        
        
    }
}

// 기존 데이터를 새 형식으로 마이그레이션
function migrateOldFavorites(adminId) {
    const migrationKey = `favoriteMigrationDone_${adminId}`;
    
    // 마이그레이션 완료 플래그 확인
    if (localStorage.getItem(migrationKey)) {
        return;
    }
    
    // 전역 마이그레이션 플래그 (모든 사용자에게 공통으로설정)
    const globalMigrationKey = 'globalFavoriteMigrationDone';
    
    // 기존 데이터가 있는지 확인
    const oldFavorites = JSON.parse(localStorage.getItem('adminFavorites')) || [];
    
    // 전역 마이그레이션이 아직 안됐고, 현재 사용자가 기존 데이터의 소유자라면 마이그레이션 수행
    if (!localStorage.getItem(globalMigrationKey) && oldFavorites.length > 0) {
        // 기존 데이터를 현재 관리자의 저장소로 복사
        const storageKey = `adminFavorites_${adminId}`;
        localStorage.setItem(storageKey, JSON.stringify(oldFavorites));
        
        // 기존 데이터 삭제
        localStorage.removeItem('adminFavorites');
        
        // 전역 마이그레이션 완료 표시
        localStorage.setItem(globalMigrationKey, 'true');
    }
    
    // 현재 페이지의 모든 즐겨찾기 가능 항목을 가져옴
    const stars = document.querySelectorAll('.favorite-star');
    const currentItems = Array.from(stars).map(star => ({
        title: star.getAttribute('data-title'),
        url: star.getAttribute('data-url')
    }));
    
    const storageKey = `adminFavorites_${adminId}`;
    const favorites = JSON.parse(localStorage.getItem(storageKey)) || [];
    let updated = false;
    
    // 즐겨찾기의 제목 업데이트 (URL은 동일하게 유지)
    favorites.forEach(fav => {
        const matchingItem = currentItems.find(item => item.url === fav.url);
        if (matchingItem && matchingItem.title !== fav.title) {
            fav.title = matchingItem.title;
            updated = true;
        }
    });
    
    if (updated) {
        localStorage.setItem(storageKey, JSON.stringify(favorites));
        updateFavoritesNav(adminId);
    }
    
    // 마이그레이션 완료 표시
    localStorage.setItem(migrationKey, 'true');
}