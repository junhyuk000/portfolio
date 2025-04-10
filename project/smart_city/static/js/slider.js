// static/js/slider.js

// Swiper 슬라이더 초기화 및 관련 기능
document.addEventListener('DOMContentLoaded', function() {
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
            
            // 슬라이드 효과 사용
            effect: 'slide',
            
            // 자동 재생 설정
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            
            // 네비게이션 버튼 설정 - 화살표 버튼이 컨테이너 외부에 있음
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            
            // 페이지네이션 설정
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            
            // 오버플로우 처리
            watchOverflow: true,
            
            // 슬라이더가 화면 밖으로 나가지 않도록 설정
            observer: true,
            observeParents: true,
            
            // 슬라이드 효과를 더 부드럽게 만들기 위한 설정
            grabCursor: true,
            touchRatio: 1,
            touchAngle: 45,
            simulateTouch: true,
            
            // 접근성 개선
            a11y: {
                prevSlideMessage: '이전 슬라이드',
                nextSlideMessage: '다음 슬라이드',
                paginationBulletMessage: '{{index}}번 슬라이드로 이동',
                firstSlideMessage: '첫 번째 슬라이드',
                lastSlideMessage: '마지막 슬라이드',
            },
            
            // 키보드 네비게이션 활성화
            keyboard: {
                enabled: true,
                onlyInViewport: true,
            },
            
            // 터치 네비게이션 구성
            touchEventsTarget: 'container',
            touchStartPreventDefault: false, // 모바일에서 스크롤 방해 방지
        });
        
        // 슬라이더가 변경될 때 자동으로 포커스 유지
        swiper.on('slideChange', function() {
            const activeSlide = swiper.slides[swiper.activeIndex];
            if (activeSlide) {
                const slideImg = activeSlide.querySelector('img');
                if (slideImg) {
                    slideImg.setAttribute('aria-current', 'true');
                }
            }
        });
        
        // 전역 변수로 스와이퍼 인스턴스 저장
        window.swiperInstance = swiper;
        
        return swiper;
    };
    
    // 이미지를 로드한 후 슬라이더 업데이트
    const updateSwiperAfterImagesLoaded = () => {
        const swiperContainer = document.querySelector('.swiper-container');
        if (!swiperContainer || !window.swiperInstance) return;
        
        const slides = document.querySelectorAll('.swiper-slide img');
        if (slides.length === 0) return;
        
        let loadedImages = 0;
        
        // 모든 이미지가 로드되면 업데이트
        const imageLoaded = () => {
            loadedImages++;
            if (loadedImages === slides.length) {
                window.swiperInstance.update();
            }
        };
        
        // 각 이미지에 로드 이벤트 리스너 추가
        slides.forEach(img => {
            if (img.complete) {
                imageLoaded();
            } else {
                img.addEventListener('load', imageLoaded);
                img.addEventListener('error', imageLoaded); // 이미지 오류 시에도 처리
            }
        });
    };

    // 반응형 슬라이더 높이 조정
    const enhanceResponsiveSlider = () => {
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
        
        // 초기화
        updateSliderHeight();
        
        // 리사이즈 시 업데이트
        window.addEventListener('resize', updateSliderHeight);
    };
    
    // 슬라이더 초기화
    const swiper = initSwiper();
    
    // 슬라이더 이미지 로드 및 반응형 처리
    if (swiper) {
        updateSwiperAfterImagesLoaded();
        enhanceResponsiveSlider();
        
        // 다크모드 변경 시 스와이퍼 업데이트 (darkmode.js에서 발생하는 이벤트 수신)
        document.addEventListener('darkModeChanged', function() {
            if (window.swiperInstance) {
                window.swiperInstance.update();
            }
        });
    }
    
    // 슬라이더 함수들 외부 노출
    window.sliderManager = {
        update: function() {
            if (window.swiperInstance) {
                window.swiperInstance.update();
            }
        },
        reinitialize: function() {
            if (window.swiperInstance) {
                window.swiperInstance.destroy();
            }
            initSwiper();
            updateSwiperAfterImagesLoaded();
        }
    };
});