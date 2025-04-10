//static\js\chat.js

document.addEventListener('DOMContentLoaded', function() {
    initFloatingChat();
});

function initFloatingChat() {
    const floatingChat = document.getElementById('floatingChat');
    const chatIcon = document.getElementById('chatIcon');
    const closePanel = document.getElementById('closePanel');
    const chatPanel = document.getElementById('chatPanel');
    const startChat = document.getElementById('startChat');
    
    if (!floatingChat || !chatIcon || !closePanel || !chatPanel) return;
    
    // 채팅 아이콘 클릭 이벤트
    chatIcon.addEventListener('click', function(e) {
        floatingChat.classList.toggle('active');
        const expanded = floatingChat.classList.contains('active');
        chatIcon.setAttribute('aria-expanded', expanded);
        chatPanel.setAttribute('aria-hidden', !expanded);
        
        if (expanded) {
            setTimeout(() => closePanel.focus(), 300);
        }
    });
    
    // 닫기 버튼 클릭 이벤트
    closePanel.addEventListener('click', function(e) {
        e.stopPropagation(); // 이벤트 버블링 방지
        floatingChat.classList.remove('active');
        chatIcon.setAttribute('aria-expanded', false);
        chatPanel.setAttribute('aria-hidden', true);
        chatIcon.focus();
    });
    
    // 실시간 채팅 시작 버튼 클릭 이벤트
    if (startChat) {
        startChat.addEventListener('click', function(e) {
            e.stopPropagation(); // 이벤트 버블링 방지
            showChatInterface();
        });
    }
    
    // ESC 키로 패널 닫기
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && floatingChat.classList.contains('active')) {
            floatingChat.classList.remove('active');
            chatIcon.setAttribute('aria-expanded', false);
            chatPanel.setAttribute('aria-hidden', true);
        }
    });
    
    // 채팅 인터페이스 표시 함수
    function showChatInterface() {
        const panelBody = document.querySelector('.panel-body');
        const panelTitle = document.getElementById('panelTitle');
        const mainBackButton = document.getElementById('mainBackButton');
        
        if (!panelBody || !panelTitle || !mainBackButton) return;
        
        // 제목 변경 및 뒤로가기 버튼 표시
        panelTitle.textContent = "실시간 채팅 상담";
        mainBackButton.style.display = "flex";
        
        // 원래 패널 내용 저장
        const originalContent = panelBody.innerHTML;
        
        // 패널 내용을 채팅 인터페이스로 교체 - 페이드인 적용
        panelBody.innerHTML = '<div class="chat-interface-container chat-fade-in"></div>';
        
        const chatContainer = panelBody.querySelector('.chat-interface-container');
        
        // 즉시 채팅 인터페이스 표시 (딜레이 없음)
        chatContainer.innerHTML = `
            <div id="chatMessages" class="chat-messages">
                <div class="message system">
                    <div class="message-content">안녕하세요! 스마트 도시 고객센터입니다. 무엇을 도와드릴까요?</div>
                </div>
            </div>
            <div class="chat-input-container">
                <textarea id="chatInput" placeholder="메시지를 입력하세요..." rows="2"></textarea>
                <button id="sendMessage">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        `;
        
        // 채팅 메시지 전송 기능 설정
        setupChatMessageSending();
        
        // 뒤로가기 버튼 이벤트 설정
        mainBackButton.addEventListener('click', function(e) {
            e.stopPropagation(); // 이벤트 버블링 방지
            
            // 원래 내용으로 복원
            panelBody.innerHTML = originalContent;
            
            // 제목 원래대로 변경, 뒤로가기 버튼 숨김
            panelTitle.textContent = "고객 지원";
            mainBackButton.style.display = "none";
            
            // 이벤트 다시 연결
            const newStartChat = document.getElementById('startChat');
            if (newStartChat) {
                newStartChat.addEventListener('click', function(e) {
                    e.stopPropagation();
                    showChatInterface();
                });
            }
        });
    }
    
    // 채팅 메시지 전송 기능 설정
    function setupChatMessageSending() {
        const chatInput = document.getElementById('chatInput');
        const sendMessage = document.getElementById('sendMessage');
        const chatMessages = document.getElementById('chatMessages');
        
        if (!chatInput || !sendMessage || !chatMessages) return;
        
        // 메시지 전송 기능
        function sendUserMessage() {
            const message = chatInput.value.trim();
            if (!message) return;
            
            // 사용자 메시지 추가
            addMessage(message, 'user');
            chatInput.value = '';
            chatInput.style.height = 'auto';
            
            // 자동 응답 (데모용)
            setTimeout(() => {
                const responses = [
                    "안녕하세요! 무엇을 도와드릴까요?",
                    "문의하신 내용에 대해 확인해보겠습니다.",
                    "더 필요한 정보가 있으실까요?",
                    "다른 질문이 있으시면 언제든지 물어봐주세요.",
                    "현재 담당자가 확인 중입니다. 잠시만 기다려주세요."
                ];
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addMessage(randomResponse, 'bot');
            }, 1000);
        }
        
        // 메시지 추가 함수
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = text;
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            
            // 스크롤을 맨 아래로 이동
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // 이벤트 리스너 등록
        sendMessage.addEventListener('click', function(e) {
            e.stopPropagation();
            sendUserMessage();
        });
        
        // 엔터키 입력 이벤트
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendUserMessage();
            }
            
            // 입력창 높이 자동 조절
            setTimeout(() => {
                chatInput.style.height = 'auto';
                chatInput.style.height = Math.min(chatInput.scrollHeight, 100) + 'px';
            }, 0);
        });
        
        // 초기 포커스 설정
        chatInput.focus();
    }
    
    // 패널 내부 클릭 시 이벤트 버블링 방지
    chatPanel.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    // 카카오톡 링크 업데이트
    const kakaoLink = document.querySelector('.support-option.kakao .option-button');
    if (kakaoLink) {
        kakaoLink.href = "https://open.kakao.com/o/s68XDGmh";
    }
}