from gevent import monkey
monkey.patch_all()  # 🚀 최상단에서 패치 적용

from flask import Flask, url_for, render_template, send_from_directory, redirect, session, request
from flask_mail import Mail, Message
from project.Total_Employment_site.site import employment_site
from project.MovieAPP.movie import popcornapp, manager
from functools import wraps
from flask_session import Session # 서버용 세션 모듈
from datetime import timedelta
import os

app = Flask(__name__, static_folder="static")
app.secret_key = 'your_secret_key'  # 세션 암호화 키

# app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static','uploads')
app.config['USER_IMAGE_FOLDER'] = "/home/junhyuk/flask_app/portfolio/project/MovieAPP/static/user_image"

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 영구 유지여부 False 브라우저가 열려있는 동안만 저장, True 일땐 브라우저 닫아도 기본값(1달)으로 정해져있는 시간동안 저장
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1) # timedelta를 활용하여 유지시간 설정
# 세션 저장 방식
app.config['SESSION_TYPE'] = 'filesystem'
# 보안 세션ID 서명
app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = 'your_secret_key'


# 이메일 설정
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'junhyuk733@gmail.com'  # Gmail 주소
app.config['MAIL_PASSWORD'] = 'ghhg ivfl nqzv ntci'  # Gmail 앱 비밀번호
app.config['MAIL_DEFAULT_SENDER'] = 'junhyuk733@gmail.com'

mail = Mail(app)


# flask_session 초기화
Session(app)


# 블루프린트 등록
app.register_blueprint(employment_site)
app.register_blueprint(popcornapp)

try:
    manager.initialize_movies_data()
    print("✅ 영화 데이터 초기화 성공!")
except Exception as e:
    print(f"⚠️ 영화 데이터 초기화 실패: {e}")



# 정적 파일을 외부에서 접근할 수 있도록 라우트 추가
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/pdf/<path:filename>')
def pdf_file(filename):
    return send_from_directory('static/pdf', filename)

@app.route('/css/<path:filename>')
def css_file(filename):
    return send_from_directory('static/css', filename)

@app.route('/images/<path:filename>')
def img_file(filename):
    return send_from_directory('static/images', filename)

@app.route('/js/<path:filename>')
def js_file(filename):
    return send_from_directory('static/js', filename)

@app.route('/files/<path:filename>')
def files_file(filename):
    return send_from_directory('static/files', filename)

@app.route('/교육 내용/<path:filename>')
def port_file(filename):
    return send_from_directory('static/교육 내용', filename)




                        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['email']
    subject = request.form['subject']
    sender = request.form['sender']
    body_content = request.form['body']

    # 본문에 작성자 정보 포함
    full_body = f"<p><strong>작성자:</strong> {sender}</p><hr>" + body_content

    msg = Message(subject, recipients=[recipient])
    msg.html = full_body

    try:
        mail.send(msg)
        return render_template("email_success.html", recipient=recipient, sender=sender, subject=subject)
    except Exception as e:
        return render_template("email_fail.html", error=str(e))

@app.route('/employment_intro')
def employment_intro():
    return render_template('employment_intro.html', active_tab='contact')
   




if __name__=='__main__':
    
    app.run(host='0.0.0.0',port='80', debug=True)