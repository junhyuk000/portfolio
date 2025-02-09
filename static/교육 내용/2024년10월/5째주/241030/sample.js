

function setCookie(name, value, days){
    let expires = "";
    if (days){
        let date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires +"; path=/";
}

function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for(let i=0; i<ca.length;i++){
        let c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);  //substring() == slice
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const messageDiv = document.getElementById("message");

    if (username === "test" && password === "1234") {
        setCookie("user",username, 7);
        messageDiv.textContent = "로그인 성공!";
        window.location.href = "welcome.html";
    }else{
        messageDiv.textContent = "아이디 또는 비밀번호가 잘못되었습니다.";
    }
}

window.onload = function(){
    const user = getCookie("user");
    if (user){
        document.getElementById("login-form").innerHTML = "<h2>" + user + "님 환영합니다!</h2><button onclick='logout()'>로그아웃</button>";
    }
};

function logout() {
    setCookie("user", "", -1);
    window.location.href = "01.html";
}