// static/js/about.js

// window.onload를 사용하여 모든 리소스가 로드된 후 실행
window.onload = function() {
    // 요소 선택
    const aboutHeader = document.querySelector('.about-header');
    const aboutSections = document.querySelectorAll('.about-section');
    const teamSection = document.querySelector('.about-team');
    const teamMembers = document.querySelectorAll('.team-member');

    // 모든 요소 초기 설정 - 위에서 아래로 등장하는 효과를 위한 설정
    function setupInitialState(element) {
        if (!element) return;
        element.style.opacity = '0';
        element.style.transform = 'translateY(-20px)'; // 위에서 아래로 내려오는 애니메이션
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    }

    // 모든 요소 초기화 (CSS에서 이미 opacity: 0을 설정했으므로 transform만 설정)
    // 초기 상태 설정을 CSS에서 하므로 여기서는 transition과 transform만 설정
    function setupTransitionOnly(element) {
        if (!element) return;
        element.style.transform = 'translateY(-20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    }

    // 요소들의 transition 설정
    setupTransitionOnly(aboutHeader);
    aboutSections.forEach(section => setupTransitionOnly(section));
    if (teamSection) setupTransitionOnly(teamSection);
    teamMembers.forEach(member => setupTransitionOnly(member));

    // 요소 표시 함수
    function showElement(element) {
        if (!element) return;
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }

    // 요소들을 순차적으로 표시
    function showElementsSequentially() {
        // 헤더 표시
        setTimeout(() => {
            showElement(aboutHeader);
        }, 100); // 더 빠르게 시작

        // 각 섹션 순차적으로 표시
        aboutSections.forEach((section, index) => {
            setTimeout(() => {
                showElement(section);
            }, 400 + (index * 400)); // 지연 시간 단축
        });

        // 팀 섹션이 존재하면
        if (teamSection) {
            // 모든 섹션 이후에 팀 섹션 표시
            const teamSectionDelay = 400 + (aboutSections.length * 400) + 200;
            setTimeout(() => {
                showElement(teamSection);
            }, teamSectionDelay);

            // 팀 멤버들 순차적으로 표시
            teamMembers.forEach((member, index) => {
                setTimeout(() => {
                    showElement(member);
                }, teamSectionDelay + 300 + (index * 200)); // 팀 섹션 이후, 각 멤버마다 지연 시간 단축
            });
        }
    }

    // 애니메이션 시작 (약간의 지연 후)
    setTimeout(showElementsSequentially, 50);
};