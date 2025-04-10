/**
 * 다크모드 기능 구현 스크립트
 * - 로컬 스토리지에 다크모드 설정 저장
 * - 페이지 로드 시 깜빡임 방지
 * - CSS 변수 기반 다크모드 전환
 */

// 페이지 로드 전 깜빡임 방지를 위한 초기화 (페이지 최상단에 실행)
(function() {
    // 로컬 스토리지에서 다크모드 설정 가져오기
    const savedDarkMode = localStorage.getItem('darkMode');
    
    // 사용자가 이전에 다크모드를 사용했거나 시스템이 다크모드인 경우
    if (savedDarkMode === 'true' || 
        (savedDarkMode === null && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      // 로딩 중 깜빡임 방지를 위해 HTML에 임시 클래스 추가
      document.documentElement.classList.add('dark-mode-preload');
      // body에도 다크모드 클래스를 미리 추가
      document.documentElement.classList.add('dark-mode');
    }
  })();
  
  // DOM이 로드된 후 실행
  document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const modeText = document.getElementById('mode-text');
    
    // 사용자 설정 불러오기 (로컬 스토리지)
    const loadUserPreference = () => {
      const savedDarkMode = localStorage.getItem('darkMode');
      
      // 저장된 설정이 없으면 시스템 기본 설정 사용
      if (savedDarkMode === null) {
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
      }
      
      return savedDarkMode === 'true';
    };
    
    // 다크모드 적용 함수
    const applyDarkMode = (isDarkMode) => {
      if (isDarkMode) {
        document.documentElement.classList.add('dark-mode'); // html 요소에 클래스 추가
        document.body.classList.add('dark-mode'); // body에도 클래스 추가
        if (modeText) modeText.textContent = '라이트모드';
      } else {
        document.documentElement.classList.remove('dark-mode'); // html 요소에서 클래스 제거
        document.body.classList.remove('dark-mode'); // body에서도 클래스 제거
        if (modeText) modeText.textContent = '다크모드';
      }
      
      // 다크모드 상태 저장
      localStorage.setItem('darkMode', isDarkMode);
    };
    
    // 초기 상태 설정
    const isDarkMode = loadUserPreference();
    applyDarkMode(isDarkMode);
    
    // 체크박스 상태와 darkmode 동기화
    if (darkModeToggle) {
      darkModeToggle.checked = isDarkMode;
      
      // 토글 이벤트 리스너 추가
      darkModeToggle.addEventListener('change', function() {
        applyDarkMode(this.checked);
      });
    }
    
    // 시스템 다크모드 변경 감지
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      // 사용자가 아직 직접 설정하지 않은 경우에만 시스템 설정을 따름
      if (localStorage.getItem('darkMode') === null) {
        const isDarkMode = e.matches;
        applyDarkMode(isDarkMode);
        if (darkModeToggle) darkModeToggle.checked = isDarkMode;
      }
    });
    
    // 다크모드 프리로드 클래스 제거 (페이지 로드 완료 후)
    // 더 안정적인 로딩을 위해 시간을 약간 늘림
    setTimeout(() => {
      document.documentElement.classList.remove('dark-mode-preload');
    }, 100);
  });
  
  // 로그인 모달 관련 스크립트
  document.addEventListener('DOMContentLoaded', function() {
    // 모든 로그인 필요 링크에 이벤트 리스너 추가
    const loginRequiredLinks = document.querySelectorAll('.login-required');
    const loginAlert = document.getElementById('login-alert');
    const closeAlertBtn = document.getElementById('close-alert-btn');
    const goToLoginBtn = document.getElementById('go-to-login');
    
    if (loginRequiredLinks.length > 0 && loginAlert) {
      loginRequiredLinks.forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          
          // 모달 표시
          loginAlert.style.display = 'flex';
          setTimeout(() => {
            loginAlert.classList.add('show');
            loginAlert.querySelector('.alert-content').classList.add('show');
          }, 10);
        });
      });
    }
    
    // 닫기 버튼
    if (closeAlertBtn) {
      closeAlertBtn.addEventListener('click', function() {
        loginAlert.classList.remove('show');
        setTimeout(() => {
          loginAlert.style.display = 'none';
        }, 400);
      });
    }
    
    // 로그인 하기 버튼
    if (goToLoginBtn) {
      goToLoginBtn.addEventListener('click', function() {
        window.location.href = '/login';
      });
    }
    
    // 모달 외부 클릭 시 닫기
    if (loginAlert) {
      loginAlert.addEventListener('click', function(e) {
        if (e.target === loginAlert) {
          loginAlert.classList.remove('show');
          setTimeout(() => {
            loginAlert.style.display = 'none';
          }, 400);
        }
      });
    }
    
    // 플래시 메시지 자동 숨김
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
      flashMessages.forEach(message => {
        message.classList.add('show');
        
        // 5초 후 자동으로 사라짐
        setTimeout(() => {
          message.classList.remove('show');
          setTimeout(() => {
            message.remove();
          }, 500);
        }, 5000);
      });
    }
  });