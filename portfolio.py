from flask import Flask, url_for, render_template, send_from_directory, redirect, session, request
from project.Total_Employment_site.site import employment_site
from project.MovieAPP.movie import popcornapp, manager
from functools import wraps
from flask_session import Session # 서버용 세션 모듈
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 암호화 키

# app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static','uploads')
app.config['USER_IMAGE_FOLDER'] = os.path.join(app.root_path, 'static','user_image')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 영구 유지여부 False 브라우저가 열려있는 동안만 저장, True 일땐 브라우저 닫아도 기본값(1달)으로 정해져있는 시간동안 저장
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1) # timedelta를 활용하여 유지시간 설정
# 세션 저장 방식
app.config['SESSION_TYPE'] = 'filesystem'
# 보안 세션ID 서명
app.config['SESSION_USE_SIGNER'] = True
app.config['SECRET_KEY'] = 'your_secret_key'

# flask_session 초기화
Session(app)


# 블루프린트 등록
app.register_blueprint(employment_site)
app.register_blueprint(popcornapp)

manager.initialize_movies_data()

users = {
    '신준혁': {'password':'1234', 'role':'admin'},
    'user0': {'password':'0000', 'role':'guest'},
    'hyundai': {'password':'1234', 'role':'user'}
}




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user'] not in users:
            return '로그인이 필요합니다.', 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    if session['role'] == 'admin':
        return render_template('Home.html')
    elif session['role'] == 'user':
        return render_template('user.html')
    return render_template('Home.html')


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

@app.route('/교육 내용/<path:filename>')
def port_file(filename):
    return send_from_directory('static/교육 내용', filename)

@app.route('/project.html')
@login_required
def direct1_file():
    return render_template('project.html')

    

@app.route('/education.html')
@login_required
def education():
    return render_template('education.html')

    

@app.route('/resume.html')
@login_required
def resume():
    return render_template('resume.html')

   

@app.route('/introduction.html')
@login_required
def introduction():
    return render_template('introduction.html')

    

@app.route('/career.html')
@login_required
def career():
    return render_template('career.html')
 

@app.route('/html포토폴리오/교육 내용.html')
def re_education():
    return redirect(url_for('education'))



@app.route('/user')
@app.route('/user.html')
@login_required
def user():
    return render_template('user.html')


                        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@app.route('/Home.html')
@login_required
def home():
    return render_template('Home.html')

@app.route('/employment_intro')
def employment_intro():
    return render_template('employment_intro.html', active_tab='contact')
   


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')  # ✅ KeyError 방지
        password = request.form.get('password')
        if user_id in users and users[user_id]['password'] == password:
            session['user'] = user_id 
            session['role'] = users[user_id]['role']  # 사용자 역할 저장
            return redirect(url_for('dashboard'))
        return f'로그인 실패<br><br><a href="/login">login</a>'
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)  # session 내 user 삭제
    return redirect(url_for('index'))




if __name__=='__main__':
    app.run(host='0.0.0.0',port='8080', debug=True)