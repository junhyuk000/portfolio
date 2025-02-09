import mysql.connector
from datetime import datetime
from flask import flash
import pymysql
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import json
import re



class DBManager:
    def __init__(self):
        # MySQL 데이터베이스 연결
        self.connection = None
        self.cursor = None
    
    def initialize_movies_data(self):
        """ 앱 시작 시 한 번만 실행할 함수 """
        self.moives_info()
        self.movies_images()
        self.update_filename_in_db("movies")

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host='121.165.69.56',
                    user='junhyuk',
                    password='1234',
                    database='port_movie_db',
                    connection_timeout=600  # 10분
                )
                self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")
            
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
#--------------------------기본값으로 설정--------------------------------★    
        
    ### 회원가입
    def regsiter_user(self, name, id, password,user_ip, filename):
        try:
            self.connect()
            sql = f"INSERT INTO users (name, user_id, password, user_ip,filename) values (%s, %s, password(%s),%s, %s)"
            values = (name, id, password, user_ip,filename)  # 튜플형태
            self.cursor.execute(sql, values)

            self.connection.commit()

            flash("계정등록이 성공적으로 완료되었습니다!", "success")
            return True
        except mysql.connector.Error as error:
        # except pymysql.IntegrityError as e:    
            print(f"계정 등록 실패: {error}")
            # flash("중복된 아이디가 존재 합니다.", "error")
            return False
        finally:  
            self.disconnect() 
    
    ### 로그인
    def login_user(self, id, password):
        try:
            self.connect()
            sql = f"SELECT * FROM users where user_id = %s and password=password(%s) and deleted_at IS NULL"
            values = (id, password)
            self.cursor.execute(sql,values)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            flash("계정 조회 실패", "error")
            print(f"계정 조회 실패: {error}")
            return []
        finally:
            self.disconnect()
    
    ### 회원가입시 id 중복 확인
    def duplicate_user(self,id):
        try:
            self.connect()
            sql = f"SELECT * FROM users where user_id = %s and deleted_at IS NULL"
            value = (id,)
            self.cursor.execute(sql,value)
            result = self.cursor.fetchone()
            if result:
                return True
            else:
                sql = "SELECT * FROM "
                return False
        except mysql.connector.Error as error:
            print(f"게시글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()
    
    ### 해당 id 유저정보 가져오기
    def get_user_by_id(self,id):
        try:
            self.connect()
            sql = f"SELECT * FROM users WHERE user_id = %s and deleted_at IS NULL"
            value = (id,) # 튜플에 값이 한개만 들어갈때 ,해줘야됨 
            self.cursor.execute(sql, value)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")
            return None
        finally:
            self.disconnect()     

    ### 해당 id 유저 비밀번호 변경
    def get_user_edit_password(self, id, password):
        try:
            self.connect()
            sql = f"UPDATE users SET `password` = PASSWORD(%s) WHERE `user_id`=%s and deleted_at IS NULL"
            value = (password,id) # 튜플에 값이 한개만 들어갈때 ,해줘야됨 
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            print(f"게시글 조회수 증가 실패: {error}")
            return False
        finally:
            self.disconnect()   

    ### 해당 id 유저 회원 탈퇴
    def delete_user(self, id):
        try:
            self.connect()
            sql = f"UPDATE users SET deleted_at = NOW() WHERE user_id = %s;"
            value = (id,) # 튜플에 값이 한개만 들어갈때 ,해줘야됨 
            self.cursor.execute(sql, value)
            self.connection.commit()
            flash("회원 탈퇴 성공!",'success')
            return True
        except mysql.connector.Error as error:
            print(f"유저 삭제 실패: {error}")
            return False
        finally:
            self.disconnect()

    ### 모든 리뷰 정보 가져오기
    def get_all_posts(self):
        try:
            self.connect()
            sql = f"SELECT * FROM posts where deleted_at IS NULL"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"게시글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()
        
    ### 리뷰 추가하기    
    def insert_post(self, title, content, filename, userid, username, rating, spoiler, movie_title, movie_id):
        try:
            self.connect()

            # 1️⃣ 게시글 추가
            sql = """
                INSERT INTO posts (title, content, filename, created_at, userid, username, rating, spoiler, movie_title, movie_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (title, content, filename, datetime.now(), userid, username, rating, spoiler, movie_title, movie_id)
            self.cursor.execute(sql, values)

            # 2️⃣ users 테이블 업데이트 (posts +1, popcorns +5)
            self.cursor.execute("""
                UPDATE users 
                SET posts = IFNULL(posts, 0) + 1, 
                    popcorns = IFNULL(popcorns, 0) + 5 
                WHERE user_id = %s
            """, (userid,))

            self.connection.commit()  # ✅ 트랜잭션 커밋
            return True

        except mysql.connector.Error as error:
            print(f"게시글 추가 실패: {error}")
            if self.connection:
                self.connection.rollback()  # ❌ 오류 발생 시 롤백
            return False

        finally:
            self.disconnect()
       
    ### 선택된 리뷰 자세히 보기     
    def get_post_by_id(self, id):
        try:
            self.connect()
            sql = f"SELECT * FROM posts WHERE id = %s"
            value = (id,) # 튜플에 값이 한개만 들어갈때 ,해줘야됨 
            self.cursor.execute(sql, value)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")
            return None
        finally:
            self.disconnect()
            
    ### 리뷰 수정
    def update_post(self, id, title, content, filename):
        try:
            self.connect()
            if filename:
                sql = f"UPDATE posts SET title = %s, content =%s, filename= %s WHERE id =%s"
                values = (title, content, filename, id)  # 튜플형태
            else:
                sql = f"UPDATE posts SET title = %s, content =%s WHERE id =%s"
                values = (title, content, id)  # 튜플형태
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 정보 수정 실패: {error}")
            return False
        finally:
            self.disconnect()
    
    ### 리뷰 삭제
    def delete_post(self, post_id, user_id):
        try:
            self.connect()

            # 1️⃣ 리뷰 삭제 (deleted_at 업데이트)
            sql = "UPDATE posts SET deleted_at = NOW() WHERE id = %s;"
            value = (post_id,)
            self.cursor.execute(sql, value)

            # 2️⃣ users 테이블 업데이트 (posts -1, popcorns -5, popcorns는 최소 0 이상)
            self.cursor.execute("""
                UPDATE users 
                SET posts = GREATEST(IFNULL(posts, 0) - 1, 0), 
                    popcorns = GREATEST(IFNULL(popcorns, 0) - 5, 0) 
                WHERE user_id = %s
            """, (user_id,))

            self.connection.commit()  # ✅ 트랜잭션 커밋
            print("✅ 리뷰 삭제 및 users 테이블 업데이트 완료.")
            return True

        except mysql.connector.Error as error:
            print(f"❌ 리뷰 삭제 실패: {error}")
            if self.connection:
                self.connection.rollback()  # ❌ 오류 발생 시 롤백
            return False

        finally:
            self.disconnect()
    
    ### 리뷰 조회수     
    def increment_hits(self, id):
        try:
            self.connect()
            sql = f"UPDATE posts SET views = views +1 WHERE id = %s"
            value = (id,) # 튜플에 값이 한개만 들어갈때 ,해줘야됨 
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            print(f"게시글 조회수 증가 실패: {error}")
            return False
        finally:
            self.disconnect()     

    ### 리뷰 추천수        
    def recommend_post(self, id):
        try:
            # 데이터베이스 연결
            self.connect()

            # 추천 수 증가
            sql = f"UPDATE posts SET recommend = recommend + 1 WHERE id = %s"
            value = (id,)
            self.cursor.execute(sql, value)
            self.connection.commit()

            # 추천 완료 메시지
            flash('추천이 성공적으로 처리되었습니다!', 'success')

        except Exception as e:
            # 오류 처리
            print(f"Error: {e}")
            flash('추천 처리 중 오류가 발생했습니다.', 'danger')
        finally:
            self.disconnect()   
    
    ### 리뷰 신고수
    def report_post_count(self, id):
        try:
            # 데이터베이스 연결
            self.connect()

            # 신고수 증가
            sql = f"UPDATE posts SET report = report + 1 WHERE id = %s"
            value = (id,)
            self.cursor.execute(sql, value)
            self.connection.commit()

            # 신고고 완료 메시지
            flash('신고가 성공적으로 처리되었습니다!', 'success')

        except Exception as e:
            # 오류 처리
            print(f"Error: {e}")
            flash('신고 처리 중 오류가 발생했습니다.', 'danger')
        finally:
            self.disconnect()   
    
    
    ### 신고 내용 저장
    def report_post(self, post_id,reporter_id, content, reason_code,movie_title,writer_id):
        try:
            # 데이터베이스 연결
            self.connect()

            # 신고 내용 저장
            sql = f"INSERT INTO reports (post_id,reporter_id,movie_title,writer_id, content, reason_code) VALUES (%s, %s, %s, %s, %s, %s)"
            value = (post_id,reporter_id, movie_title,writer_id, content, reason_code)
            self.cursor.execute(sql, value)
            self.connection.commit()

            flash('신고가 성공적으로 접수되었습니다.', 'success')
        except Exception as e:
            print(f"Error: {e}")
            flash('신고 처리 중 문제가 발생했습니다.', 'danger')
        finally:
            self.disconnect()


    ### 영화 이미지 requests, BeautifulSoup을 활용하여 제목과 함께 저장    
    def movies_images(self):
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%98%81%ED%99%94+%EC%88%9C%EC%9C%84"
        base_dir = os.path.abspath(os.getcwd())
        save_dir = os.path.join(base_dir, "static", "images")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 먼저 전체 제목 리스트를 가져옴 (Processing row에서 사용하는 방식과 동일)
        items = soup.select('div.list_image_info.type_pure_top div ul:nth-child(1) li')
        titles = []
        for item in items[:10]:
            # Processing row에서 사용하는 것과 동일한 방식으로 제목 추출
            title = item.select_one('strong').text.strip()
            titles.append(title)

        # 이미지 태그 찾기
        img_tags = soup.find_all('img')[:10]

        # 제목과 이미지를 함께 처리
        for idx, (title, img_tag) in enumerate(zip(titles, img_tags)):
            try:
                img_url = img_tag.get('src')
                if not img_url:
                    print(f"No image URL found for {title}")
                    continue

                img_url = requests.compat.urljoin(url, img_url)
                print(f"Downloading {img_url}...")

                img_response = requests.get(img_url)
                img_response.raise_for_status()

                # 파일 이름 생성
                sanitized_title = self.sanitize_filename(title)
                img_name = f"{sanitized_title}.jpg"
                img_path = os.path.join(save_dir, img_name)

                # 디버깅 로그
                print(f"Original title: {title}")
                print(f"Sanitized title: {sanitized_title}")
                print(f"Image name: {img_name}")
                print(f"Image path: {img_path}")

                with open(img_path, 'wb') as file:
                    file.write(img_response.content)
                print(f"Saved: {img_path}")

            except Exception as e:
                print(f"Error processing movie: {e}")
                import traceback
                print(traceback.format_exc())

    ### 파일 이름 유효성 체크
    def sanitize_filename(self, filename):
        # Windows에서 사용할 수 없는 문자 처리
        invalid_chars = '<>:"/\\|?*'
        # filename = filename.replace(':', '_')  # 콜론을 언더스코어로 변경
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()  # 앞뒤 공백 제거

    ### 이미지파일 movies 테이블에 업데이트
    def update_filename_in_db(self, table_name):
        """
        데이터베이스에서 title 컬럼에 해당하는 filename 값을 업데이트합니다.
        """
        try:
            self.connect()

            # 이미지 파일 목록 가져오기
            image_files = os.listdir("static/images")
            noimage_path = os.path.join('static/images', 'noimage.jpg')

            # noimage.jpg 확인
            if 'noimage.jpg' not in image_files:
                print("Warning: 'noimage.jpg' 파일이 존재하지 않습니다.")

            # SQL로 title 데이터 가져오기
            self.cursor.execute(f"SELECT id, title FROM {table_name}")
            rows = self.cursor.fetchall()

            for row in rows:
                title = row['title']
                sanitized_title = self.sanitize_filename(title)
                matched_file = None

                # 이미지 파일 이름 매칭
                for image_file in image_files:
                    file_name, _ = os.path.splitext(image_file)
                    if sanitized_title[:15] == file_name[:15]:
                        matched_file = image_file
                        break

                # 이미지가 없으면 noimage.jpg 사용
                if not matched_file:
                    matched_file = "noimage.jpg"

                # SQL UPDATE
                sql = f"""
                    UPDATE {table_name}
                    SET filename = %s
                    WHERE title = %s;
                """
                values = (matched_file, title)
                self.cursor.execute(sql, values)

            # 변경 사항 저장
            self.connection.commit()
            print(f"{self.cursor.rowcount} rows updated in {table_name} table.")

        except mysql.connector.Error as error:
            print(f"Error updating filename: {error}")
        finally:
            self.disconnect()

    ### KOBIS사이트에서 일별 박스오피스 및 영화 상세정보 API 가져와서 PANDAS를 활용하여 필요한 데이터 추출    
    def moives_info(self):
        servicekey = '8a40bbeb34b2e89293f764616dee588c'
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        yesterday_formatted = yesterday.strftime('%Y%m%d')

        url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={servicekey}&targetDt={yesterday_formatted}'
        res = requests.get(url)
        today_datas = res.json()

        t_datas = []
        for data in today_datas["boxOfficeResult"]["dailyBoxOfficeList"]:
            movie_data = {
                "rank": data["rank"],
                "title": data["movieNm"],
                "release_date": data["openDt"],
                "t_sales": data["salesAmt"],
                "c_sales": data["salesAcc"],
                "t_audience": data["audiCnt"],
                "c_audience": data["audiAcc"],
                "moviecd": data["movieCd"]
            }
            t_datas.append(movie_data)

        m_infos = []
        for data in t_datas:
            url1 = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={servicekey}&movieCd={data["moviecd"]}'
            res1 = requests.get(url1)
            movie_infos = res1.json()

            # ✅ API 응답 확인
            print(f"🎬 {data['title']} ({data['moviecd']}) API 응답:", movie_infos)

            # ✅ KeyError 방지
            if "movieInfoResult" not in movie_infos or "movieInfo" not in movie_infos["movieInfoResult"]:
                print(f"❌ 'movieInfoResult' 또는 'movieInfo' 키 없음! (movieCd: {data['moviecd']})")
                continue

            movie_data = movie_infos["movieInfoResult"]["movieInfo"]

            nations = movie_data.get("nations", [])
            nations = nations[0]["nationNm"] if nations else "Unknown"

            genres = movie_data.get("genres", [])
            genres = genres[0]["genreNm"] if genres else "Unknown"

            # 영화 데이터에서 감독 정보 가져오기 (한 명만)
            directors = movie_data.get("directors", [])
            director = directors[0]["peopleNm"] if directors else "Unknown"

            # 영화 데이터에서 배우 정보 가져오기 (모든 배우)
            actors = movie_data.get("actors", [])
            actor_names = ", ".join([actor["peopleNm"] for actor in actors]) if actors else "Unknown"


            result = {
                "moviecd": data["moviecd"],
                "nations": nations,
                "genres": genres,
                "director": director,
                "actors": actor_names
            }
            m_infos.append(result)

        df1 = pd.DataFrame(t_datas)
        df2 = pd.DataFrame(m_infos)
        df3 = pd.merge(df1, df2, on='moviecd', how='inner')
        print("🔍 [DEBUG] df1 데이터 개수:", len(df1))
        print(df1.head())  # ✅ df1이 비어있는지 확인
        print("🔍 [DEBUG] df2 데이터 개수:", len(df2))
        print(df2.head())  # ✅ df2가 비어있는지 확인

        df3['c_sales'] = df3['c_sales'].fillna(0).astype('int64')
        df3['rank'] = df3['rank'].astype(int)
        df3['t_audience'] = df3['t_audience'].astype(int)
        df3['c_audience'] = df3['c_audience'].astype(int)
        df3['t_sales'] = df3['t_sales'].astype(int)

        print("🔍 [DEBUG] insert_data_with_no_duplicates() 함수 실행 직전")
        print(f"🔍 [DEBUG] df3 데이터 개수: {len(df3)}")
        print(f"🔍 [DEBUG] df3 샘플 데이터:\n{df3.head()}")
        self.insert_data_with_no_duplicates(df3)

    def insert_data_with_no_duplicates(self, df):
        print("🔍 [DEBUG] insert_data_with_no_duplicates() 호출 전 데이터 확인")
        print(f"🔍 df3 행 개수: {len(df)}")
        print(f"🔍 df3 샘플 데이터:\n{df.head()}")

        try:
            self.connect()
            for _, row in df.iterrows():
                print(f"📌 Checking whether to INSERT or UPDATE for {row['title']} ({row['director']})")

                # ✅ 중복 확인 (title + director)
                check_sql = """
                    SELECT id FROM movies 
                    WHERE BINARY TRIM(title) = BINARY TRIM(%s) 
                    AND BINARY TRIM(director) = BINARY TRIM(%s)
                """
                self.cursor.execute(check_sql, (row['title'].strip(), row['director'].strip()))
                existing_record = self.cursor.fetchone()

                # ✅ `rank`값이 정수인지 확인
                movie_rank = int(row['rank']) if pd.notna(row['rank']) else 0

                # ✅ 기본값 처리 (None 방지)
                values = (
                    movie_rank,                      # rank
                    row['title'].strip(),           # title
                    str(row['genres']).strip(),     # genres
                    row['director'].strip(),        # director
                    str(row['nations']).strip(),    # nations
                    None,                           # rating (기본값 NULL)
                    None,                           # reviews (기본값 NULL)
                    int(row['t_audience']),         # t_audience
                    int(row['c_audience']),         # c_audience
                    int(row['t_sales']),            # t_sales
                    int(row['c_sales']),            # c_sales
                    row.get('filename', 'noimage.jpg'),  # filename
                    row['release_date'],            # release_date
                    str(row['actors']).strip() if 'actors' in row else ""  # actors 추가 (None 방지)
                )

                if existing_record:
                    print(f"🛠 Updating: {row['title']} ({row['director']})")

                    # 🔍 UPDATE 전 데이터 확인
                    self.cursor.execute(
                        "SELECT * FROM movies WHERE BINARY TRIM(title) = BINARY TRIM(%s) AND BINARY TRIM(director) = BINARY TRIM(%s)",
                        (row['title'].strip(), row['director'].strip())
                    )
                    before_update = self.cursor.fetchone()
                    print(f"Before Update: {before_update}")

                    update_sql = """
                        UPDATE movies
                        SET rank = %s,
                            title = %s,
                            genres = %s,
                            director = %s,
                            nations = %s,
                            rating = %s,
                            reviews = %s,
                            t_audience = %s,
                            c_audience = %s,
                            t_sales = %s,
                            c_sales = %s,
                            filename = %s,
                            release_date = %s,
                            actors = %s,  -- ✅ actors 추가
                            input_date = CURRENT_TIMESTAMP
                        WHERE BINARY TRIM(title) = BINARY TRIM(%s) 
                        AND BINARY TRIM(director) = BINARY TRIM(%s)
                    """
                    
                    update_values = values + (row['title'].strip(), row['director'].strip())
                    print(f"🔹 Update Values: {update_values}")

                    self.cursor.execute(update_sql, update_values)
                    self.connection.commit()

                    # 🔍 UPDATE 후 데이터 확인
                    self.cursor.execute(
                        "SELECT * FROM movies WHERE BINARY TRIM(title) = BINARY TRIM(%s) AND BINARY TRIM(director) = BINARY TRIM(%s)",
                        (row['title'].strip(), row['director'].strip())
                    )
                    after_update = self.cursor.fetchone()
                    print(f"After Update: {after_update}")
                    print(f"🛠 Updated rows: {self.cursor.rowcount}")

                else:
                    print(f"🆕 Will attempt INSERT for {row['title']} ({row['director']})")
                    insert_sql = """
                        INSERT INTO movies 
                        (rank, title, genres, director, nations, rating, reviews, 
                        t_audience, c_audience, t_sales, c_sales, filename, release_date, actors)  -- ✅ actors 추가
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    print(f"🎯 Insert Values: {values}")
                    self.cursor.execute(insert_sql, values)
                    self.connection.commit()
                    print(f"✅ Inserted: {row['title']} ({row['director']})")

                print("✅ Database update completed successfully.")

        except mysql.connector.Error as error:
            print(f"❌ Database error: {error}")
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
        finally:
            self.disconnect()



    ### 오늘 날짜의 영화 정보 가져오기
    def get_all_movies(self):
        try:
            self.connect()
            seoul_tz = timezone('Asia/Seoul')
            today_date = datetime.now(seoul_tz).strftime('%Y-%m-%d')  # 한국 시간 기준 날짜
            sql = "SELECT * FROM movies WHERE DATE(input_date) = %s order by rank asc"
            self.cursor.execute(sql, (today_date,))
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"영화 데이터 조회 실패: {error}")
            return []
        finally:
            self.disconnect()

    def get_all_popcorns_movies(self):
        """모든 영화 정보를 popcorns가 많은 순으로 가져오기"""
        try:
            self.connect()
            query = """
                SELECT m.id, m.title, m.director, m.rating, m.reviews, m.filename, m.c_audience, 
                    COALESCE(l.popcorns, 0) AS popcorns
                FROM movies m
                LEFT JOIN (
                    SELECT movie_id, SUM(popcorns) AS popcorns 
                    FROM lots 
                    GROUP BY movie_id
                ) l ON m.id = l.movie_id
                ORDER BY popcorns DESC
            """
            self.cursor.execute(query)
            movies = self.cursor.fetchall()
            return movies
        except mysql.connector.Error as error:
            print(f"영화 데이터 조회 실패: {error}")
            return []
        finally:
            self.disconnect()

    ### 댓글 추가
    def insert_comment(self, post_id, user_id, user_name, content):
        try:
            self.connect()

            # 1️⃣ 댓글 추가
            sql = """
                INSERT INTO comments (post_id, user_id, user_name, content, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (post_id, user_id, user_name, content, datetime.now())
            self.cursor.execute(sql, values)

            # 2️⃣ users 테이블 업데이트 (comments +1, popcorns +3)
            self.cursor.execute("""
                UPDATE users 
                SET comments = IFNULL(comments, 0) + 1, 
                    popcorns = IFNULL(popcorns, 0) + 2 
                WHERE user_id = %s
            """, (user_id,))

            self.connection.commit()  # ✅ 트랜잭션 커밋
            print("✅ 댓글 추가 및 users 테이블 업데이트 완료.")
            return True

        except mysql.connector.Error as error:
            print(f"❌ 댓글 추가 실패: {error}")
            if self.connection:
                self.connection.rollback()  # ❌ 오류 발생 시 롤백
            return False

        finally:
            self.disconnect()

    ### 모든 댓글 정보 가져오기
    def get_all_comments(self):
        try:
            self.connect()
            sql = f"SELECT * FROM comments where deleted_at IS NULL"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"댓글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()
            
    ### 해당 id 데이터 가져오기
    def get_comment_by_id(self, id):
        try:
            self.connect()
            sql = f"SELECT * FROM comments WHERE id = %s and deleted_at IS NULL"
            value = (id,) # 튜플에 값이 한개만 들어갈때 ,해줘야됨 
            self.cursor.execute(sql, value)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")
            return None
        finally:
            self.disconnect()
        
    def delete_comment(self, comment_id, user_id):
        try:
            self.connect()

            print(f"🔍 [DEBUG] delete_comment() 실행 - 댓글 ID: {comment_id}, 사용자 ID: {user_id}")

            # 댓글 삭제 SQL 실행
            sql = "UPDATE comments SET deleted_at = NOW() WHERE id = %s AND deleted_at IS NULL;"
            value = (comment_id,)
            self.cursor.execute(sql, value)

            print(f"🔍 [DEBUG] 실행된 rowcount: {self.cursor.rowcount}")  # ✅ rowcount 확인

            # ✅ rowcount가 0이면 삭제되지 않은 것 → 원인 분석 필요
            if self.cursor.rowcount == 0:
                print(f"⚠ Warning: 댓글 ID {comment_id} 삭제 실패 (이미 삭제되었거나 존재하지 않음)")
                return False

            # 2️⃣ users 테이블 업데이트 (comments -1, popcorns -3, popcorns는 최소 0 이상)
            self.cursor.execute("""
                UPDATE users 
                SET comments = GREATEST(IFNULL(comments, 0) - 1, 0), 
                    popcorns = GREATEST(IFNULL(popcorns, 0) - 3, 0) 
                WHERE user_id = %s
            """, (user_id,))

            self.connection.commit()  # ✅ 트랜잭션 커밋
            print(f"✅ 댓글 삭제 완료: ID {comment_id}, 사용자 {user_id}")
            return True

        except mysql.connector.Error as error:
            print(f"❌ 댓글 삭제 실패: {error}")
            if self.connection:
                self.connection.rollback()  # ❌ 오류 발생 시 롤백
            return False

        finally:
            self.disconnect()


            
    def comment_post_count(self, id):
        try:
            # 데이터베이스 연결
            self.connect()
            # 댓글수 증가
            sql = f"UPDATE posts SET comment = comment + 1 WHERE id = %s"
            value = (id,)
            self.cursor.execute(sql, value)
            self.connection.commit()

        except Exception as e:
            # 오류 처리
            print(f"Error: {e}")
            flash('댓글 처리 중 오류가 발생했습니다.', 'danger')
        finally:
            self.disconnect()   

    def movies_reviews_count(self, title):
        try:
            # 데이터베이스 연결
            self.connect()
            # 댓글수 증가
            sql = f"UPDATE movies SET reviews = reviews + 1 WHERE title = %s"
            value = (title,)
            self.cursor.execute(sql, value)
            self.connection.commit()

        except Exception as e:
            # 오류 처리
            print(f"Error: {e}")
            flash('리뷰 카운터 처리 중 오류가 발생했습니다.', 'danger')
        finally:
            self.disconnect()   


    def update_movie_ratings_and_reviews(self):
        try:
            # 데이터베이스 연결
            self.connect()

            # 영화 제목별 평균 rating 및 리뷰 개수 계산
            self.cursor.execute("""
                SELECT 
                    movie_title,
                    AVG(rating) AS avg_rating,
                    COUNT(*) AS review_count
                FROM 
                    posts
                WHERE 
                    rating IS NOT NULL
                GROUP BY 
                    movie_title
            """)
            aggregated_data = self.cursor.fetchall()

            # movies 테이블 업데이트
            for row in aggregated_data:
                movie_title = row['movie_title']
                avg_rating = row['avg_rating']
                review_count = row['review_count']

                # 영화 제목에 해당하는 평균 rating 및 리뷰 개수 업데이트
                self.cursor.execute("""
                    UPDATE movies
                    SET rating = %s, reviews = %s
                    WHERE title = %s
                """, (avg_rating, review_count, movie_title))

            # 변경사항 커밋
            self.connection.commit()
            print("Movies table updated successfully!")

        except mysql.connector.Error as error:
            print(f"Error updating movie ratings and reviews: {error}")
        finally:
            self.disconnect()

    
    def view_reports(self):
        try:
            self.connect()

            # reports 테이블에서 데이터 가져오기
            self.cursor.execute("SELECT * FROM reports")
            return self.cursor.fetchall()

        except mysql.connector.Error as error:
            print(f"Error fetching reports: {error}")
            return "Error loading reports."

        finally:
            self.disconnect()

    def loc_ip(self, user_ip):
        url = f"https://ipinfo.io/{user_ip}?token=08f027512e9236"
        try:
            response = requests.get(url)
            data = response.json()  # JSON 응답을 딕셔너리로 변환
            
            if "loc" in data:
                return data["loc"]  # 위도, 경도 반환
            else:
                return "Location not found"

        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def popcorns_lot(self, movie_id, movie_title, user_id):
        """추첨 기능 (lots +1, popcorns -10)"""
        try:
            self.connect()

            # 🔍 사용자의 현재 popcorns 조회
            self.cursor.execute("SELECT popcorns FROM users WHERE user_id = %s", (user_id,))
            user = self.cursor.fetchone()

            if user is None:
                return "사용자를 찾을 수 없습니다!"
            
            user_popcorns = user["popcorns"] if user["popcorns"] is not None else 0

            if user_popcorns < 10:
                return "팝콘이 부족합니다!"  # 🚨 팝콘 부족 오류 반환

            # 🔍 lots 테이블 확인 (기존 데이터 있는지 체크)
            self.cursor.execute("SELECT popcorns FROM lots WHERE movie_id = %s AND user_id = %s", (movie_id, user_id))
            existing_lot = self.cursor.fetchone()

            if existing_lot:
                # 기존 항목이 있으면 popcorns 증가
                new_popcorns = existing_lot["popcorns"] + 10
                self.cursor.execute("UPDATE lots SET popcorns = %s WHERE movie_id = %s AND user_id = %s",
                                    (new_popcorns, movie_id, user_id))
            else:
                # 없으면 새로 추가
                self.cursor.execute("INSERT INTO lots (movie_id, movie_title, user_id, popcorns) VALUES (%s, %s, %s, 10)",
                                    (movie_id, movie_title, user_id))

            # 🔹 users 테이블 업데이트 (lots +1, popcorns -10)
            self.cursor.execute("UPDATE users SET lots = IFNULL(lots, 0) + 1, popcorns = popcorns - 10 WHERE user_id = %s", (user_id,))

            self.connection.commit()
            return True  # ✅ 성공

        except mysql.connector.Error as error:
            print(f"Database error: {error}")
            if self.connection:
                self.connection.rollback()
            return "데이터 처리 중 오류 발생!"

        finally:
            self.disconnect()


    def get_all_movie_data(self, page=1, per_page=20, order_by="total_audience", title="", genre="", nation="", director="", actor=""):
        """영화 데이터를 페이지네이션하여 반환하는 함수"""
        try:
            self.connect()
            
            # 오프셋 계산
            offset = (page - 1) * per_page
            
            # 기본 쿼리
            base_query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY {0} DESC) AS rank,
                    movie_title, genre, nations, director, actors, total_sales, total_audience, release_date,
                    COUNT(*) OVER() as total_count
                FROM movie_summary
                WHERE 1=1
            """.format(order_by)
            
            query_params = []
            
            if title:
                base_query += " AND movie_title LIKE %s"
                query_params.append(f"%{title}%")
            if genre:
                base_query += " AND genre LIKE %s"
                query_params.append(f"%{genre}%")
            if nation:
                base_query += " AND nations LIKE %s"
                query_params.append(f"%{nation}%")
            if director:
                base_query += " AND director LIKE %s"
                query_params.append(f"%{director}%")
            if actor:
                base_query += " AND actors LIKE %s"
                query_params.append(f"%{actor}%")
                
            # 페이지네이션 적용
            base_query += f" ORDER BY {order_by} DESC LIMIT %s OFFSET %s"
            query_params.extend([per_page, offset])
            
            self.cursor.execute(base_query, query_params)
            result = self.cursor.fetchall()
            
            if not result:
                return {"data": [], "total": 0, "pages": 0}
                
            # 전체 레코드 수 추출
            total_count = result[0]["total_count"] if isinstance(result[0], dict) else result[0][-1]
            total_pages = (total_count + per_page - 1) // per_page
            
            columns = [col[0] for col in self.cursor.description if col[0] != 'total_count']
            df = pd.DataFrame(result, columns=columns)
            
            return {
                "data": df.to_dict(orient="records"),
                "total": total_count,
                "pages": total_pages
            }
            
        except mysql.connector.Error as error:
            print(f"❌ Database error: {error}")
            return {"data": [], "total": 0, "pages": 0}
            
        finally:
            self.disconnect()

    def get_genres_and_nations(self):
        """장르 및 국가 목록 가져오기 - 쉼표로 구분된 값들을 개별 항목으로 분리"""
        try:
            self.connect()
            
            # 장르 조회 및 분리
            self.cursor.execute("SELECT DISTINCT genre FROM movie_summary WHERE genre IS NOT NULL")
            genre_results = self.cursor.fetchall()
            
            # 쉼표로 구분된 장르들을 분리하고 중복 제거
            genres = set()
            for row in genre_results:
                if isinstance(row, tuple):
                    genre_str = row[0]
                elif isinstance(row, dict):
                    genre_str = row['genre']
                
                if genre_str:
                    # 쉼표로 구분된 장르들을 분리하고 공백 제거
                    genre_list = [g.strip() for g in genre_str.split(',')]
                    genres.update(genre_list)
            
            # 국가 조회 및 분리
            self.cursor.execute("SELECT DISTINCT nations FROM movie_summary WHERE nations IS NOT NULL")
            nation_results = self.cursor.fetchall()
            
            # 쉼표로 구분된 국가들을 분리하고 중복 제거
            nations = set()
            for row in nation_results:
                if isinstance(row, tuple):
                    nation_str = row[0]
                elif isinstance(row, dict):
                    nation_str = row['nations']
                
                if nation_str:
                    # 쉼표로 구분된 국가들을 분리하고 공백 제거
                    nation_list = [n.strip() for n in nation_str.split(',')]
                    nations.update(nation_list)
            
            return {
                "genres": sorted(list(genres)),
                "nations": sorted(list(nations))
            }
            
        except mysql.connector.Error as error:
            print(f"❌ Database error: {error}")
            return {"genres": ["Unknown"], "nations": ["Unknown"]}
        
        finally:
            self.disconnect()