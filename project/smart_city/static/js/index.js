// static/js/index.js

// 홈페이지 전용 JavaScript - 다크모드 호환성 개선
document.addEventListener('DOMContentLoaded', function() {
    // 다크모드 상태 확인
    const isDarkMode = document.documentElement.classList.contains('dark-mode');
    
    // Swiper 슬라이더 초기화
    const initSwiper = () => {
        const swiperContainer = document.querySelector('.swiper-container');
        if (!swiperContainer) return null;
        
        const swiper = new Swiper('.swiper-container', {
            // 기본 설정
            slidesPerView: 1,
            spaceBetween: 0,
            loop: true,
            speed: 800,
            
            // 자동 재생 설정
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            
            // 네비게이션 버튼 설정
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            
            // 페이지네이션 설정
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            
            // 슬라이더가 화면 밖으로 나가지 않도록 설정
            observer: true,
            observeParents: true,
            
            // 접근성 개선
            a11y: {
                prevSlideMessage: '이전 슬라이드',
                nextSlideMessage: '다음 슬라이드',
                paginationBulletMessage: '{{index}}번 슬라이드로 이동',
            },
        });
        
        // 전역 변수로 스와이퍼 인스턴스 저장
        window.swiperInstance = swiper;
        
        return swiper;
    };
    
    // 반응형 슬라이더 높이 조정
    const updateSliderHeight = () => {
        const swiperContainer = document.querySelector('.swiper-container');
        if (!swiperContainer) return;
        
        // 화면 너비에 따른 높이 조정
        if (window.innerWidth <= 400) {
            swiperContainer.style.height = '250px';
        } else if (window.innerWidth <= 576) {
            swiperContainer.style.height = '350px';
        } else if (window.innerWidth <= 768) {
            swiperContainer.style.height = '450px';
        } else if (window.innerWidth <= 1200) {
            swiperContainer.style.height = '550px';
        } else {
            swiperContainer.style.height = '650px';
        }
    };
    
    // 인덱스 페이지 특화 다크모드 적용
    const applyIndexPageDarkMode = (isDarkMode) => {
        // CSS 변수 직접 설정
        if (isDarkMode) {
            document.documentElement.style.setProperty('--background-color', '#1a1a1a');
            document.documentElement.style.setProperty('--text-color', '#f0f0f0');
            document.documentElement.style.setProperty('--heading-color', '#ffffff');
            document.documentElement.style.setProperty('--widget-bg', '#333333');
            document.documentElement.style.setProperty('--widget-shadow', 'rgba(0, 0, 0, 0.2)');
            document.documentElement.style.setProperty('--widget-title', '#f0f0f0');
            document.documentElement.style.setProperty('--widget-text', '#d0d0d0');
            document.documentElement.style.setProperty('--arrow-color', '#ffffff');
            document.documentElement.style.setProperty('--arrow-hover-color', '#cccccc');
        } else {
            document.documentElement.style.setProperty('--background-color', '#f4f4f4');
            document.documentElement.style.setProperty('--text-color', '#333333');
            document.documentElement.style.setProperty('--heading-color', '#333333');
            document.documentElement.style.setProperty('--widget-bg', '#ffffff');
            document.documentElement.style.setProperty('--widget-shadow', 'rgba(0, 0, 0, 0.1)');
            document.documentElement.style.setProperty('--widget-title', '#333333');
            document.documentElement.style.setProperty('--widget-text', '#666666');
            document.documentElement.style.setProperty('--arrow-color', '#000000');
            document.documentElement.style.setProperty('--arrow-hover-color', '#333333');
        }
        
        // 헤더 요소 직접 스타일링
        const header = document.querySelector('.header');
        const headerTop = document.querySelector('.header-top');
        const headerNav = document.querySelector('.header-nav');
        const navLinks = document.querySelectorAll('.nav-link');
        const dropdowns = document.querySelectorAll('.dropdown-content');
        const dropdownLinks = document.querySelectorAll('.dropdown-content a');
        
        if (isDarkMode) {
            // 헤더 요소
            if (header) header.style.backgroundColor = '#262626';
            if (headerTop) headerTop.style.backgroundColor = '#262626';
            if (headerNav) headerNav.style.backgroundColor = '#262626';
            
            // 네비게이션 링크
            navLinks.forEach(link => {
                link.style.color = '#ffffff';
            });
            
            // 드롭다운 메뉴
            dropdowns.forEach(dropdown => {
                dropdown.style.backgroundColor = '#383838';
            });
            
            // 드롭다운 링크
            dropdownLinks.forEach(link => {
                link.style.color = '#ffffff';
            });
        } else {
            // 헤더 요소
            if (header) header.style.backgroundColor = '#ffffff';
            if (headerTop) headerTop.style.backgroundColor = '#ffffff';
            if (headerNav) headerNav.style.backgroundColor = '#ffffff';
            
            // 네비게이션 링크
            navLinks.forEach(link => {
                link.style.color = '#333333';
            });
            
            // 드롭다운 메뉴
            dropdowns.forEach(dropdown => {
                dropdown.style.backgroundColor = '#ffffff';
            });
            
            // 드롭다운 링크
            dropdownLinks.forEach(link => {
                link.style.color = '#333333';
            });
        }
        
        // 특정 위젯 스타일 적용
        const widgets = document.querySelectorAll('.widget');
        widgets.forEach(widget => {
            widget.style.backgroundColor = isDarkMode ? '#333333' : '#ffffff';
            widget.style.boxShadow = isDarkMode 
                ? '0 4px 12px rgba(0, 0, 0, 0.2)' 
                : '0 4px 12px rgba(0, 0, 0, 0.1)';
                
            const title = widget.querySelector('h3');
            if (title) title.style.color = isDarkMode ? '#f0f0f0' : '#333333';
            
            const desc = widget.querySelector('p');
            if (desc) desc.style.color = isDarkMode ? '#d0d0d0' : '#666666';
        });
        
        // 슬라이더 화살표 색상 조정
        const nextButton = document.querySelector('.swiper-button-next');
        const prevButton = document.querySelector('.swiper-button-prev');
        
        if (nextButton) nextButton.style.color = isDarkMode ? '#ffffff' : '#000000';
        if (prevButton) prevButton.style.color = isDarkMode ? '#ffffff' : '#000000';
    };
    
    // 다크모드 관리자가 있으면 강제 초기화 실행
    if (window.DarkModeManager && typeof window.DarkModeManager.forceReset === 'function') {
        window.DarkModeManager.forceReset();
    }
    
    // 현재 다크모드 상태에 맞게 적용
    applyIndexPageDarkMode(isDarkMode);
    
    // 다크모드 변경 이벤트 리스너
    document.addEventListener('darkModeChange', function(e) {
        applyIndexPageDarkMode(e.detail.isDarkMode);
        
        // 슬라이더 업데이트
        if (window.swiperInstance) {
            window.swiperInstance.update();
        }
    });
    
    // Swiper 초기화 및 반응형 조정
    initSwiper();
    updateSliderHeight();
    
    // 창 크기 변경 시 슬라이더 높이 업데이트
    window.addEventListener('resize', updateSliderHeight);
    
    // 페이지 이탈 시 다크모드 상태 저장
    window.addEventListener('beforeunload', function() {
        const isDarkMode = document.documentElement.classList.contains('dark-mode');
        localStorage.setItem('smartCityDarkMode', isDarkMode ? 'enabled' : 'disabled');
        
        // 쿠키 설정 함수 (이중 보험)
        function setCookie(name, value, days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            const expires = '; expires=' + date.toUTCString();
            document.cookie = name + '=' + value + expires + '; path=/; SameSite=Strict';
        }
        
        setCookie('smartCityDarkModeCookie', isDarkMode ? 'enabled' : 'disabled', 30);
    });
});

// 페이지 완전 로드 시 추가 조치
window.onload = function() {
    // 다크모드 상태 강제 동기화 (한 번 더)
    if (window.DarkModeManager && typeof window.DarkModeManager.forceReset === 'function') {
        window.DarkModeManager.forceReset();
    }
    
    // Swiper 업데이트
    if (window.swiperInstance) {
        window.swiperInstance.update();
    }
};