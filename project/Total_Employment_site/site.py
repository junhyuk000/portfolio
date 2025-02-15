from flask import Flask, render_template, request, Blueprint, send_from_directory, url_for, redirect,session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pymysql
import os
import urllib

### 변경부분
# ChromeDriver 경로 설정
# 리눅스 환경 
CHROMEDRIVER_PATH = "/usr/bin/chromedriver" 
# Windows 환경일 경우
# CHROMEDRIVER_PATH = r"C:\junhyuk\chromedriver-win64\chromedriver.exe"  # ChromeDriver 설치 경로 확인 후 수정


def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없이 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver 경로 설정
    chrome_driver_path = "/usr/bin/chromedriver"

    # Chrome 실행 경로 명시
    chrome_options.binary_location = "/usr/lib/chromium/chromium"

    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

###변경

# MySQL 데이터베이스 연결 설정
DB_CONFIG = {
    'host': '192.168.0.19',
    'user': 'root',
    'password': 'Wnsgur151@',
    'database': 'employment',
    'charset': 'utf8mb4'
}



# Blueprint 정의
employment_site = Blueprint('employment_site', __name__, 
                          static_folder='static', 
                          template_folder='templates', 
                          url_prefix='/employment')

# global_search_title = None

# 데이터베이스 관련 함수들은 동일하게 유지
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def save_to_db(data, table_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company VARCHAR(255),
        title VARCHAR(255),
        address VARCHAR(255),
        career VARCHAR(255),
        school VARCHAR(255),
        work_type VARCHAR(255),
        url TEXT,
        site VARCHAR(50)
    )
    """
    cursor.execute(create_table_query)
    
    # 기존 데이터 삭제
    cursor.execute(f"DELETE FROM {table_name}")

    query = f"""
    INSERT INTO {table_name} (company, title, address, career, school, work_type, url, site)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for entry in data:
        cursor.execute(query, (
            entry['company'], entry['title'], entry['address'], entry['career'],
            entry['school'], entry['work_type'], entry['url'], entry['site']
        ))

    connection.commit()
    cursor.close()
    connection.close()

def load_from_db(table_name):
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    results = list(cursor.fetchall())

    cursor.close()
    connection.close()
    return results




# 사람인 탑 10
def saramin_top():
    driver = get_chrome_driver()
    driver.set_page_load_timeout(30)
    driver.get(f"https://www.saramin.co.kr/zf_user/jobs/hot100")
    # driver.maximize_window()
    time.sleep(20)    
    company_list = []

    try:

        items = driver.find_elements(By.CSS_SELECTOR, '.list-container .list_item')[1:]
        time.sleep(2)
        
        for item in items:
            try:
                company = item.find_element(By.CSS_SELECTOR, 'div.col.company_nm > .str_tit').text
                time.sleep(2)
                title = item.find_element(By.CSS_SELECTOR, 'div.col.notification_info > div.job_tit > a.str_tit').text
                address = item.find_element(By.CSS_SELECTOR, 'div.col.recruit_info > ul > li:nth-child(1) > p').text.replace('\n', ' ')
                career = item.find_element(By.CSS_SELECTOR, 'div.col.recruit_info > ul > li:nth-child(2) > p').text.split(' · ')[0]
                school = item.find_element(By.CSS_SELECTOR, 'div.col.recruit_info > ul > li:nth-child(3) > p').text
                work_type = item.find_element(By.CSS_SELECTOR, 'div.col.recruit_info > ul > li:nth-child(2) > p').text.split(' · ')[1]
                url = item.find_element(By.CSS_SELECTOR, 'div.col.notification_info > div.job_tit > a.str_tit').get_attribute('href')
                
                company_list.append({
                    'company': company,
                    'title': title,
                    'address': address,
                    'career': career,
                    'school': school,
                    'work_type': work_type,
                    'url': url,
                    'site': '사람인'
                })

            except Exception as e:
                print(f"사람인 크롤링 중 에러 발생: {e}")
                continue

    except Exception as e:
        print(f"사람인 크롤링 중 에러 발생: {e}")
    finally:
        driver.quit()

    save_to_db(company_list, 'saramin_top')
    return render_template('top.html')

# 잡코리아 top_10
def jobkorea_top():
    company_list = []
    driver = get_chrome_driver()
    driver.set_page_load_timeout(30)
    driver.get(f"https://www.jobkorea.co.kr/top100/")
    # driver.maximize_window()
    time.sleep(1)
    try:        
        items = driver.find_elements(By.CSS_SELECTOR, 'div.rankListWrap > div.rankListArea.devSarterTab > ol > li')

        for item in items:
            try:
                company = item.find_element(By.CSS_SELECTOR, 'a.coLink').text
                title = item.find_element(By.CSS_SELECTOR, 'div.info > div.tit > a').text
                address = item.find_element(By.CSS_SELECTOR, 'div.info > div.sDsc > span:nth-child(3)').text
                career = item.find_element(By.CSS_SELECTOR, 'div.info > div.sDsc > span:nth-child(1)').text
                school = item.find_element(By.CSS_SELECTOR, 'div.info > div.sDsc > span:nth-child(2)').text
                work_type = item.find_element(By.CSS_SELECTOR, 'div.info > div.sDsc > span:nth-child(4)').text
                url = item.find_element(By.CSS_SELECTOR, 'div.info > div.tit > a').get_attribute('href')
                company_list.append({
                    'company': company,
                    'title': title,
                    'address': address,
                    'career': career,
                    'school': school,
                    'work_type': work_type,
                    'url': url,
                    'site': '잡코리아'
                })

            except Exception as e:
                pass

        time.sleep(1)
    except Exception as e:
        print(f"잡코리아 크롤링 중 에러 발생: {e}")
    finally:
        driver.quit()

    save_to_db(company_list, 'jobkorea_top')
    return company_list

# 인크루트 top 10
def incruit_top():
    driver = get_chrome_driver()
    driver.set_page_load_timeout(30)
    driver.get(f"https://job.incruit.com/jobdb_list/searchjob.asp?cate=occu&sortfield=applycnt&sortorder=1&page=1")
    # driver.maximize_window()
    time.sleep(1)

    company_list = []

    try:
        items = driver.find_elements(By.CSS_SELECTOR, '#JobList_Area > div:nth-child(2) > div.cBbslist_contenst > ul')
        for item in items[:10]:
            try:
                company = item.find_element(By.CSS_SELECTOR, 'li > div.cell_first > div.cl_top > a').text
                title = item.find_element(By.CSS_SELECTOR, 'li > div.cell_mid > div.cl_top > a').text
                address = item.find_elements(By.CSS_SELECTOR, 'li > div.cell_mid > div.cl_md > span')[2].text
                career = item.find_elements(By.CSS_SELECTOR, 'li > div.cell_mid > div.cl_md > span')[0].text
                school = item.find_elements(By.CSS_SELECTOR, 'li > div.cell_mid > div.cl_md > span')[1].text
                work_type = item.find_elements(By.CSS_SELECTOR, 'li > div.cell_mid > div.cl_md > span')[3].text
                url = item.find_element(By.CSS_SELECTOR, 'li > div.cell_mid > div.cl_top > a').get_attribute('href')
                company_list.append({
                    'company': company,
                    'title': title,
                    'address': address,
                    'career': career,
                    'school': school,
                    'work_type': work_type,
                    'url': url,
                    'site': '인크루트'
                })
                time.sleep(1)
            except Exception as e:
                pass
        time.sleep(1)
    except Exception as e:
        print(f"인크루트 크롤링 중 에러 발생: {e}")
    finally:
        driver.quit()

    save_to_db(company_list, 'incruit_top')
    return company_list

# 사람인 검색 함수
def saramin_search(search_title):
    search_title1 = search_title
    if ' ' in search_title:
        search_title = search_title.replace(' ', '%20')

    driver = get_chrome_driver()
    driver.set_page_load_timeout(30)
    driver.get(f"https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword={search_title}")
    # driver.maximize_window()
    time.sleep(5)

    company_list = []
    i = 1

    try:
        for j in range(1, 2):
            time.sleep(1)
            driver.get(f"https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword={search_title}&recruitPage={j}")
            time.sleep(2)
            items = driver.find_elements(By.CSS_SELECTOR, 'div.item_recruit')
            
            if not items:
                break
            
            for item in items:
                try:
                    company = item.find_element(By.CSS_SELECTOR, '.corp_name a').text
                    title = item.find_element(By.CSS_SELECTOR, 'a').text
                    address = item.find_element(By.CSS_SELECTOR, '.job_condition > span').text.replace('\n', ' ')
                    career = item.find_element(By.CSS_SELECTOR, 'div.job_condition > span:nth-child(2)').text
                    school = item.find_element(By.CSS_SELECTOR, 'div.job_condition > span:nth-child(3)').text
                    work_type = item.find_element(By.CSS_SELECTOR, 'div.job_condition > span:nth-child(4)').text
                    url = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    
                    company_list.append({
                        'company': company,
                        'title': title,
                        'address': address,
                        'career': career,
                        'school': school,
                        'work_type': work_type,
                        'url': url,
                        'site': '사람인'
                    })
                except Exception as e:
                    continue
            
            print(f"사람인 {i}페이지 크롤링 완료!")
            i += 1
    except Exception as e:
        print(f"사람인 크롤링 중 에러 발생: {e}")
    finally:
        driver.quit()

    save_to_db(company_list, f'saramin_{search_title1}')
    return company_list

# 잡코리아 검색 함수
def jobkorea_search(search_title):
    search_title1 = search_title
    if ' ' in search_title:
        search_title = search_title.replace(' ', '%20')

    driver = get_chrome_driver()
    driver.set_page_load_timeout(30)
    driver.get(f"https://www.jobkorea.co.kr/Search/?stext={search_title}")
    # driver.maximize_window()
    time.sleep(1)

    k = 1
    company_list = []

    try:
        for i in range(1, 2):
            next_link = f"https://www.jobkorea.co.kr/Search/?stext={search_title}&tabType=recruit&Page_No={k}"
            driver.get(next_link)
            time.sleep(2)
            items = driver.find_elements(By.CSS_SELECTOR, 'article.list-item')
            
            if not items:
                break
            
            data_extracted = False
            for item in items[:20]:
                try:
                    company = item.find_element(By.CSS_SELECTOR, 'a.corp-name-link.dev-view').text
                    title = item.find_element(By.CSS_SELECTOR, 'a.information-title-link.dev-view').text
                    address = item.find_elements(By.CSS_SELECTOR, 'ul.chip-information-group li')[3].text
                    career = item.find_elements(By.CSS_SELECTOR, 'ul.chip-information-group li')[0].text
                    school = item.find_elements(By.CSS_SELECTOR, 'ul.chip-information-group li')[1].text
                    work_type = item.find_elements(By.CSS_SELECTOR, 'ul.chip-information-group li')[2].text
                    url = item.find_element(By.CSS_SELECTOR, 'a.information-title-link.dev-view').get_attribute('href')
                    company_list.append({
                        'company': company,
                        'title': title,
                        'address': address,
                        'career': career,
                        'school': school,
                        'work_type': work_type,
                        'url': url,
                        'site': '잡코리아'
                    })
                    data_extracted = True
                except Exception as e:
                    pass

            if not data_extracted:
                break
            
            print(f"잡코리아 {i}페이지 크롤링 완료!")
            k += 1
            time.sleep(1)
    except Exception as e:
        print(f"잡코리아 크롤링 중 에러 발생: {e}")
    finally:
        driver.quit()

    save_to_db(company_list, f'jobkorea_{search_title1}')
    return company_list

# 인크루트 검색 함수
def incruit_search(search_title):
    search_title1 = search_title
    encoded_string = urllib.parse.quote(search_title)

    driver = get_chrome_driver()
    driver.set_page_load_timeout(30)
    driver.get(f"https://search.incruit.com/list/search.asp?col=job&kw={encoded_string}")
    # driver.maximize_window()
    time.sleep(1)

    k = 0
    company_list = []

    try:
        for i in range(1, 2):
            next_link = f"https://search.incruit.com/list/search.asp?col=job&kw={encoded_string}&startno={k}"
            driver.get(next_link)
            time.sleep(2)
            items = driver.find_elements(By.CSS_SELECTOR, 'ul.c_row')

            if not items:
                break

            data_extracted = False
            for item in items:
                try:
                    company = item.find_element(By.CSS_SELECTOR, '.cell_first .cl_top a.cpname').text
                    title = item.find_element(By.CSS_SELECTOR, '.cell_mid .cl_top a').text
                    address = item.find_elements(By.CSS_SELECTOR, '.cl_md span')[2].text
                    career = item.find_elements(By.CSS_SELECTOR, '.cl_md span')[0].text
                    school = item.find_elements(By.CSS_SELECTOR, '.cl_md span')[1].text
                    work_type = item.find_elements(By.CSS_SELECTOR, '.cl_md span')[3].text
                    url = item.find_element(By.CSS_SELECTOR, '.cell_mid .cl_top a').get_attribute('href')
                    company_list.append({
                        'company': company,
                        'title': title,
                        'address': address,
                        'career': career,
                        'school': school,
                        'work_type': work_type,
                        'url': url,
                        'site': '인크루트'
                    })
                    data_extracted = True
                    time.sleep(1)
                except Exception as e:
                    pass

            if not data_extracted:
                break

            print(f"인크루트 {i}페이지 크롤링 완료!")
            k += 30
            time.sleep(1)
    except Exception as e:
        print(f"인크루트 크롤링 중 에러 발생: {e}")
    finally:
        driver.quit()

    save_to_db(company_list, f'incruit_{search_title1}')
    return company_list


# 라우트 수정
@employment_site.route('/')
def index():
    return render_template('employment_index.html', active_tab='home')

@employment_site.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        if not search_query:
            return "검색어를 입력해주세요."
        
        global global_search_title
        global_search_title = search_query

        
        # 각 사이트별 검색 및 크롤링
        # saramin_search(search_query)
        jobkorea_search(search_query)
        incruit_search(search_query)
        
        # 검색 결과 페이지로 리다이렉트
        return redirect(url_for('employment_site.total'))
    
    return render_template('search.html', active_tab='search')

@employment_site.route('/refresh_top10')
def refresh_top10():
    # Top 10 데이터 새로 크롤링
    # saramin_top()
    jobkorea_top()
    incruit_top()
    return redirect(url_for('employment_site.top10'))

@employment_site.route('/top10')
def top10():
    # saramin_results = list(load_from_db('saramin_top'))
    jobkorea_results = list(load_from_db('jobkorea_top'))
    incruit_results = list(load_from_db('incruit_top'))

    all_results = jobkorea_results + incruit_results # saramin_results + jobkorea_results + incruit_results
    return render_template('top.html', results=all_results, active_tab='top10')

@employment_site.route('/total')
def total():
    if not global_search_title:
        return redirect(url_for('employment_site.search'))
    
    # saramin_results = load_from_db(f'saramin_{global_search_title}')
    jobkorea_results = load_from_db(f'jobkorea_{global_search_title}')
    incruit_results = load_from_db(f'incruit_{global_search_title}')

    all_results = jobkorea_results + incruit_results #saramin_results + jobkorea_results + incruit_results
    return render_template('total.html', results=all_results, search_query=global_search_title, active_tab='total')

@employment_site.route('/saramin')
def saramin():
    if not global_search_title:
        return redirect(url_for('employment_site.search'))
    
    results = load_from_db(f'saramin_{global_search_title}')
    return render_template('saramin.html', results=results, search_query=global_search_title, active_tab='saramin')

@employment_site.route('/jobkorea')
def jobkorea():
    if not global_search_title:
        return redirect(url_for('employment_site.search'))
    
    results = load_from_db(f'jobkorea_{global_search_title}')
    return render_template('jobkorea.html', results=results, search_query=global_search_title, active_tab='jobkorea')

@employment_site.route('/incruit')
def incruit():
    if not global_search_title:
        return redirect(url_for('employment_site.search'))
    
    results = load_from_db(f'incruit_{global_search_title}')
    return render_template('incruit.html', results=results, search_query=global_search_title, active_tab='incruit')

@employment_site.route('/contact')
def contact():
    return render_template('contact.html', active_tab='contact')




# 정적 파일 제공 라우트
@employment_site.route('/css/<path:filename>')
def css_file(filename):
    directory = os.path.join(os.path.dirname(__file__), 'static/css')
    return send_from_directory(directory, filename)

@employment_site.route('/js/<path:filename>')
def js_file(filename):
    directory = os.path.join(os.path.dirname(__file__), 'static/js')
    return send_from_directory(directory, filename)

@employment_site.route('/images/<path:filename>')
def img_file(filename):
    directory = os.path.join(os.path.dirname(__file__), 'static/images')
    return send_from_directory(directory, filename)

@employment_site.route('/fonts/<path:filename>')
def fonts_file(filename):
    directory = os.path.join(os.path.dirname(__file__), 'static/fonts')
    return send_from_directory(directory, filename)