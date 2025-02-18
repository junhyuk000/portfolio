from flask import Flask, url_for, render_template, send_from_directory, jsonify ,request, redirect, session,flash, Blueprint, current_app
from functools import wraps
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import DBManager
import pandas as pd
import joblib
import re


# Blueprint 정의
popcornapp = Blueprint('popcornapp', __name__, 
                          static_folder='static', 
                          template_folder='templates', 
                          url_prefix='/popcornapp')

manager = DBManager()

# 모델 경로 설정
TFIDF_PATH = "/home/junhyuk/flask_app/portfolio/project/MovieAPP/static/model/tfidf.pkl"
MODEL_PATH = "/home/junhyuk/flask_app/portfolio/project/MovieAPP/static/model/SA_lr_best.pkl"

# 모델 로드
if os.path.exists(TFIDF_PATH) and os.path.exists(MODEL_PATH):
    tfidf_vectorizer = joblib.load(TFIDF_PATH)  # TF-IDF 벡터라이저 로드
    text_mining_model = joblib.load(MODEL_PATH)  # 감성 분석 모델 로드
    print("✅ 모델이 성공적으로 로드되었습니다.")
else:
    tfidf_vectorizer = None
    text_mining_model = None
    print("❌ 모델 파일을 찾을 수 없습니다.")

### images 폴더 static/images 폴더로 연결
@popcornapp.route('/images/<path:filename>')
def img_file(filename):
    return send_from_directory('static/images', filename)

# 정적 폴더에서 폰트 파일 제공
@popcornapp.route('/static/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory('static/fonts', filename)

### js 폴더 static/js 폴더로 연결
@popcornapp.route('/js/<path:filename>')
def js_file(filename):
    return send_from_directory('static/js', filename)

### user_image 폴더 static/user_image 폴더로 연결
@popcornapp.route('/user_image/<path:filename>')
def user_img_file(filename):
    return send_from_directory('static/user_image', filename)

### uploads 폴더 static/uploads폴더로 연결
@popcornapp.route('/uploads/<path:filename>')
def uploads_file(filename):
    return send_from_directory('static/uploads', filename)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('popcornapp.login'))
        return f(*args, **kwargs)
    return decorated_function

### 로그인
@popcornapp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        id = request.form.get('userid')
        password = request.form.get('password')
        user = manager.login_user(id, password)
        if user:
            session['id'] = id
            session['name'] = user['name']
            session['filename'] = user['filename']
            
            return f'<script>alert("로그인 성공!");location.href="{url_for("popcornapp.movies")}"</script>'
        else:
            flash("로그인 실패!", 'error')
    return render_template('movie_login.html')



### 회원가입
@popcornapp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        id = request.form.get('userid')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        file = request.files['file']
        
        filename = file.filename if file else None
        user_image_folder = "/app/static/user_image"

        if filename:
            file_path = os.path.join(user_image_folder, filename)
            file.save(file_path)
            
        if manager.duplicate_user(id):
            flash("중복된 아이디가 존재합니다.",'error')
            return redirect(url_for('popcornapp.register'))

        if password == confirm_password:
            manager.regsiter_user(name, id, password,user_ip,filename)
            return redirect(url_for('popcornapp.login'))
        return flash("계정 등록 실패,400", "error")
    return render_template('movie_register.html')


@popcornapp.route('/logout')
def delete_session_data():
    session.pop('id', None)  # 특정 키만 삭제
    session.pop('name', None)
    session.pop('filename', None)
    flash("로그아웃 되었습니다.", "success")
    return redirect(url_for('popcornapp.login'))

### 내정보
@popcornapp.route('/myinfo')
def myinfo():
    id = session['id']
    user = manager.get_user_by_id(id)
    return render_template('movie_myinfo.html',user=user)

@popcornapp.route('/userinfo/<user_id>')
def user_info(user_id):
    id = session['id']
    user = manager.get_user_by_id(user_id)
    return render_template('movie_myinfo.html',user=user,id=id)

### 회원 탈퇴
@popcornapp.route('/delete_user')
def delete_user():
    id = session['id']
    if manager.delete_user(id):
        session.clear()
        return f'<script>alert("회원탈퇴 성공!");location.href="{url_for("popcornapp.login")}"</script>' # 스크립트로 alert알람창 띄우기
    else:
        return f'<script>alert("회원탈퇴 실패!");location.href="{url_for("popcornapp.movies")}"</script>'
    
### 회원 탈퇴(신고 추방)
@popcornapp.route('/user/delete/<user_id>')
def report_user(user_id):
    if manager.delete_user(user_id):
        flash(f"{user_id}계정이 삭제되었습니다.",'success')
        return redirect(request.referrer or url_for('popcornapp.movie_report'))
    else:
        flash(f"{user_id}계정 삭제를 실패했습니다.",'error')
        return redirect(request.referrer or url_for('popcornapp.movie_report'))

### 비밀번호 변경
@popcornapp.route('/edit_password', methods=['GET','POST'])
def edit_password():
    if request.method=='POST':
        id = request.form.get('userid')
        password = request.form.get('password')
        user = manager.get_user_by_id(id)
        if user['user_id'] == request.form.get('userid') and user['name'] == request.form.get('username'):
            if manager.get_user_edit_password(id, password):
                return f'<script>alert("비밀번호 변경 성공!");location.href="{url_for("popcornapp.login")}"</script>'
            return f'<script>alert("비밀번호 변경 실패!, 아이디 혹은 이름이 다릅니다.");location.href="{url_for("popcornapp.login")}"</script>'
    return render_template('movie_edit_password.html')

### 상영중인 영화 당일 랭킹순으로 화면에 표현
@popcornapp.route('/movies')
@popcornapp.route('/')
def movies():
    manager.update_movie_ratings_and_reviews()
    movies = manager.get_all_movies()
    movies_info = []
    for movie in movies:
        print(movie)
        movies_info.append({'id':movie['id'],"title":movie['title'],"rank":movie['rank'],"filename":movie['filename'],"rating":movie['rating'],"reviews":movie['reviews']})

    movie_infos = manager.get_all_movies()
    page_title = 'Movie_Ranks'
    title = [movie_info['title'] for movie_info in movie_infos]
    t_sales = [movie_info['t_sales'] for movie_info in movie_infos]
    c_sales = [movie_info['c_sales'] for movie_info in movie_infos]
    t_audience = [movie_info['t_audience'] for movie_info in movie_infos]
    c_audience = [movie_info['c_audience'] for movie_info in movie_infos]

    # 전체 데이터를 JSON으로 전달
    movies_data = [
        {
            "title": movie_info['title'],
            "t_sales": movie_info['t_sales'],
            "c_sales": movie_info['c_sales'],
            "t_audience": movie_info['t_audience'],
            "c_audience": movie_info['c_audience']
        }
        for movie_info in movie_infos
    ]

    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr) # 공인 ip 가져오기
    loc = manager.loc_ip(user_ip)
    return render_template('movie_movies.html', movies_info=movies_info, 
        page_title = page_title,
        movies_data=movies_data,
        title=title,
        t_sales=t_sales,
        c_sales=c_sales,
        t_audience=t_audience,
        c_audience=c_audience,
        loc = loc)



### 해당영화 리뷰
@popcornapp.route('/reviews/<title>/<movie_id>')
def review(title,movie_id):
    all_posts = manager.get_all_posts()
    posts=[]
    for post in all_posts:
        if post['movie_title'] == title:
            posts.append(post)  
    page = int(request.args.get('page', 1))  # 쿼리 파라미터에서 페이지 번호 가져오기
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = posts[start:end]
    # 총 페이지 수 계산
    total_pages = (len(posts) + per_page - 1) // per_page
    return render_template('movie_review.html',title=title, movie_id=movie_id, posts=paginated_data, page=page, total_pages=total_pages)


### 선택한 리뷰 상세히 보기
@popcornapp.route('/post/<title>/<int:id>')
@login_required
def view_post(id,title):
    post = manager.get_post_by_id(id)
    views = manager.increment_hits(id)
    text = post['content']
    if not text:
        return jsonify({"error": "텍스트를 입력하세요."}), 400

    # 모델이 로드되지 않았다면 오류 반환
    if tfidf_vectorizer is None or text_mining_model is None:
        return jsonify({"error": "모델이 로드되지 않았습니다."}), 500

    # 📌 1. 입력 텍스트 전처리 (한글만 추출)
    text_processed = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(text)
    text_cleaned = " ".join(text_processed) if text_processed else ""

    # 📌 2. 전처리된 텍스트를 TF-IDF 벡터화
    if text_cleaned:
        text_vectorized = tfidf_vectorizer.transform([text_cleaned])

        # 📌 3. 감성 분석 모델 예측
        prediction = text_mining_model.predict(text_vectorized)
        sentiment = "긍정" if prediction[0] == 1 else "부정"
    else:
        sentiment = "중립"  # 내용이 없거나 분석 불가한 경우
    all_comments = manager.get_all_comments()
    comments = []
    for comment in all_comments:
        if comment['post_id'] == id:
            comments.append(comment)
    return render_template('movie_view.html',title=title,post=post, views=views, comments=comments, id=id, sentiment = sentiment)


### 리뷰 추가
### 파일업로드: method='POST' enctype="multipart/form-data" type='file accept= '.png,.jpg,.gif
@popcornapp.route('/post/add/<movie_title>/<movie_id>', methods=['GET', 'POST'])
@login_required
def add_post(movie_title,movie_id):
    userid = session.get('id')
    username = session.get('name')
    user_img = session.get('filename')

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('review_content')
        rating = request.form.get('rating')
        spoiler = bool(request.form.get('spoiler'))
        file = request.files.get('file')
        filename = None
        if file and file.filename:
            filename = file.filename
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        if manager.insert_post(title, content, filename, userid, username, rating, spoiler, movie_title, movie_id):
            flash("리뷰가 성공적으로 추가되었습니다!", "success")
            return redirect(f'/popcornapp/reviews/{movie_title}/{movie_id}')
        else:
            flash("리뷰 추가 실패!", "error")
            return redirect(request.url)

    return render_template('movie_review_add.html', movie_title=movie_title, movie_id=movie_id )

### 리뷰 수정(수정)
@popcornapp.route('/post/edit/<movie_title>/<int:id>', methods=['GET', 'POST'])
def edit_post(movie_title, id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        
        filename = file.filename if file else None
        
        if filename:
            file_path = os.path.join(popcornapp.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        
        # 게시글 정보를 업데이트
        if manager.update_post(id, title, content, filename):
            flash("업데이트 성공!", "success")
            return redirect(f'/popcornapp/post/{movie_title}/{id}')
        return flash("게시글 수정 실패,400", 'error')  # 실패 시 400 에러 반환

    # GET 요청: 게시글 정보를 가져와 폼에 표시
    post = manager.get_post_by_id(id)
    if post:
        return render_template('movie_edit.html', movie_title = movie_title, id=id, post=post)  # 수정 페이지 렌더링
    return flash("게시글을 찾을 수 없습니다.404", 'error')

### 리뷰 삭제
@popcornapp.route('/post/delete/<int:id>')
def delete_post(id):
    post = manager.get_post_by_id(id)
    user_id = session.get('id')
    if post:
        file = post.get('filename')
        if file:
            file_path = os.path.join(popcornapp.config['UPLOAD_FOLDER'], file)
            os.remove(file_path)
            flash("file삭제",'success')
            if manager.delete_post(id,user_id):
                flash("게시물 삭제 성공!","success")
                return redirect(f'/popcornapp/reviews/{post["movie_title"]}/{post["movie_id"]}')
            return f'<script>alert("파일 삭제 성공! 게시물 삭제 실패!");location.href="{url_for("register")}"</script>' # 스크립트로 alert알람창 띄우기
        else:
            if manager.delete_post(id,user_id):
                flash("게시물 삭제 성공!","success")
                return redirect(f'/popcornapp/reviews/{post["movie_title"]}/{post["movie_id"]}')
        flash("삭제실패",'error')
    
    return redirect(url_for('view'))

# ### 영화 랭킹(일일 관객수, 누적 관객수, 일일 매출액, 누적 매출액) 시각화
# @app.route('/movie_ranks')
# def movie_ranks():
#     movie_infos = manager.get_all_movies()
#     page_title = 'Movie_Ranks'
#     title = [movie_info['title'] for movie_info in movie_infos]
#     t_sales = [movie_info['t_sales'] for movie_info in movie_infos]
#     c_sales = [movie_info['c_sales'] for movie_info in movie_infos]
#     t_audience = [movie_info['t_audience'] for movie_info in movie_infos]
#     c_audience = [movie_info['c_audience'] for movie_info in movie_infos]

#     # 전체 데이터를 JSON으로 전달
#     movies_data = [
#         {
#             "title": movie_info['title'],
#             "t_sales": movie_info['t_sales'],
#             "c_sales": movie_info['c_sales'],
#             "t_audience": movie_info['t_audience'],
#             "c_audience": movie_info['c_audience']
#         }
#         for movie_info in movie_infos
#     ]
#     return render_template(
#         'movie_ranks.html',
#         page_title = page_title,
#         movies_data=movies_data,
#         title=title,
#         t_sales=t_sales,
#         c_sales=c_sales,
#         t_audience=t_audience,
#         c_audience=c_audience
#     )        

# ### 카카오 지도로 사용자 공인 ip를 활용하여 근처 영화관 검색 
# @app.route('/movie_map')
# def movie_map():
#     user_ip = request.headers.get('X-Forwarded-For', request.remote_addr) # 공인 ip 가져오기
#     loc = manager.loc_ip(user_ip)
#     return render_template('movie_map.html', loc= loc)

### 영화별 예고편
@popcornapp.route('/movie_youtube/<title>')
def movie_youtube(title):
    return render_template('movie_youtube.html',title=title)

@popcornapp.route('/post/recommend/<int:post_id>/<title>')
def recommend_post(post_id,title):
    manager.recommend_post(post_id)
    # 추천 후 목록 페이지로 리디렉션
    return redirect(request.referrer or url_for('popcornapp.view_post', id=id))


@popcornapp.route('/post/report/<movie_title>/<int:post_id>/<writer_id>', methods=['GET', 'POST'])
def report_post(movie_title,post_id,writer_id):
    if request.method == 'POST':
        # 신고 내용 및 사유 저장
        content = request.form.get('content')
        reason_code = request.form.get('reason')  # 체크박스에서 선택한 값
        reporter_id = request.form.get('user_id')
        if not content or not reason_code:
            flash('신고 내용을 작성하고 사유를 선택해주세요.', 'danger')
            return redirect(url_for('popcornapp.report_post',movie_title=movie_title, post_id=post_id,writer_id=writer_id))
        manager.report_post_count(post_id)
        manager.report_post(post_id,reporter_id, content, reason_code,movie_title,writer_id)

        return redirect(url_for('popcornapp.movies'))  # 신고 후 목록 페이지로 리디렉션
    return render_template('movie_report.html',movie_title=movie_title, post_id=post_id,writer_id=writer_id)

@popcornapp.route('/movie_review_rank')
def movie_review_rank():
    posts = manager.get_all_posts()
    tops = []
    recommend = []
    for post in posts:
        tops.append({
            'id':post['id'],
            'user_id': post['userid'],
            'title': post['title'],
            'movie_title': post['movie_title'],
            'views': post['views'],
            'recommend': post['recommend'],
            'comments': post['comment']
            })
    top_views = sorted(tops, key=lambda x: x['views'], reverse=True)[:10]
    top_recommend = sorted(tops, key=lambda x: x['recommend'], reverse=True)[:10]
    top_comments = sorted(tops, key=lambda x: x['comments'], reverse=True)[:10]
    return render_template('movie_review_rank.html', top_views = top_views, top_recommend=top_recommend, top_comments=top_comments)



@popcornapp.route('/post/<int:id>/comment', methods = ['POST'])
def movie_review_comment(id):
    # 댓글 저장 로직
    # 예: DB에 댓글 추가
    content = request.form.get('content')
    if content:
        # DB에 저장하는 로직 (예시)
        manager.insert_comment(post_id=id, user_id=session['id'],user_name=session['name'], content=content)
    manager.comment_post_count(id)
    # 사용자가 왔던 페이지로 리다이렉트
    return redirect(request.referrer or url_for('popcornapp.view_post', id=id))

@popcornapp.route('/post/comment_delete/<int:post_id>/<int:comment_id>', methods=['GET'])
def delete_comment(post_id, comment_id):
    print(f"🔍 [DEBUG] 댓글 삭제 요청 - 댓글 ID: {comment_id}, 게시글 ID: {post_id}")

    # 로그인 체크
    user_id = session.get('id')
    if not user_id:
        flash("로그인이 필요합니다!", "error")
        return redirect(request.referrer or url_for('popcornapp.view_post', id=post_id))

    # 댓글 정보 조회
    comment = manager.get_comment_by_id(comment_id)
    print(f"🔍 [DEBUG] 댓글 정보: {comment}")

    if not comment:
        flash("❌ 존재하지 않는 댓글입니다!", "error")
        return redirect(request.referrer or url_for('popcornapp.view_post', id=post_id))

    # 권한 체크 (작성자 또는 관리자)
    if user_id != comment['user_id'] and user_id != 'admin':
        flash("❌ 삭제 권한이 없습니다!", "error")
        return redirect(request.referrer or url_for('popcornapp.view_post', id=post_id))

    # 댓글 삭제 시도
    success = manager.delete_comment(comment_id, user_id)
    
    if success:
        flash("✅ 댓글이 삭제되었습니다.", "success")
    else:
        flash("❌ 댓글 삭제에 실패했습니다.", "error")

    return redirect(request.referrer or url_for('popcornapp.view_post', id=post_id))


@popcornapp.route('/reports')
def movie_report():
    reports = manager.view_reports()
    return render_template('movie_reports.html',reports=reports)

@popcornapp.route('/show_movie_about')
def show_movie_about():
    return render_template('movie_about.html')

@popcornapp.route('/movie_about')
def movie_about():
    try:
        # 절대 경로로 CSV 파일 읽기
        base_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "static/csv/movie_data_2010_to_present.csv")
        data = pd.read_csv(file_path)

        # 날짜 데이터 변환
        data['date'] = pd.to_datetime(data['date'], format='%Y%m%d', errors='coerce')
        data['year'] = data['date'].dt.year

        # 코로나 전후 평균값 계산
        pre_covid = data[data['year'] < 2020]
        post_covid = data[data['year'] >= 2020]
        pre_covid_avg = pre_covid['audiCnt'].mean()
        post_covid_avg = post_covid['audiCnt'].mean()

        # 넷플릭스 전후 평균값 계산
        pre_netflix = data[data['year'] < 2016]
        post_netflix = data[data['year'] >= 2016]
        pre_netflix_avg = pre_netflix['audiCnt'].mean()
        post_netflix_avg = post_netflix['audiCnt'].mean()

        # 연도별 평균 관람객 계산
        yearly_avg = data.groupby('year')['audiCnt'].mean().reset_index()

        # JSON 데이터 반환
        response = {
            "pre_post_covid": [pre_covid_avg, post_covid_avg],
            "pre_post_netflix": [pre_netflix_avg, post_netflix_avg],
            "yearly_avg": yearly_avg.to_dict(orient='records')
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@popcornapp.route('/movie_notice')
def movie_notice():
    return render_template('movie_notice.html')

@popcornapp.route('/movie_popcorns', methods=['GET', 'POST'])
def movie_popcorns():
    if request.method == 'POST':
        data = request.json
        movie_id = data.get("movie_id")
        movie_title = data.get("movie_title")
        user_id = session.get('id')  # ✅ 올바른 세션 접근

        if user_id is None:
            return jsonify({"error": "로그인이 필요합니다!"}), 401  # 로그인 필요

        result = manager.popcorns_lot(movie_id, movie_title, user_id)

        if isinstance(result, str):  # 에러 메시지 반환 시
            return jsonify({"error": result}), 400
        else:
            return jsonify({"message": f"🎟️ {movie_title}가 추첨되었습니다! (팝콘 -10)"}), 200

    # `popcorns`가 많은 순서로 정렬된 영화 리스트 가져오기
    movies = manager.get_all_popcorns_movies()
    return render_template('movie_popcorns.html', movies=movies)

@popcornapp.route('/all_movies')
def all_movies():
    movies = manager.get_all_movie_data()
    filters = manager.get_genres_and_nations()
    return render_template('movie_all_movies.html', data=movies, filters = filters)

@popcornapp.route("/filter", methods=["GET"])
def filter_data():
    page = int(request.args.get("page", 1))
    order_by = request.args.get("order_by", "total_audience")
    title = request.args.get("title", "").strip()
    genre = request.args.get("genre", "").strip()
    nation = request.args.get("nation", "").strip()
    director = request.args.get("director", "").strip()
    actor = request.args.get("actor", "").strip()

    result = manager.get_all_movie_data(
        page=page,
        order_by=order_by,
        title=title,
        genre=genre,
        nation=nation,
        director=director,
        actor=actor
    )

    return jsonify(result)
