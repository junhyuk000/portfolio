import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import os

# 한글 세팅
#r'C:/junhyuk/python/fonts/DoHyeon-Regular.ttf'
fontpath = "C:/Windows/Fonts/malgun.ttf"
mask_path = r'C:/junhyuk/python/img/star.jpg'
output_path = r'C:/junhyuk/Portfolio/project/Total_Employment_site/static/images/word2.png'

# 경로 점검
if not os.path.exists(fontpath):
    raise FileNotFoundError(f"폰트 파일이 없습니다: {fontpath}")

if not os.path.exists(mask_path):
    raise FileNotFoundError(f"마스크 이미지 파일이 없습니다: {mask_path}")

output_dir = os.path.dirname(output_path)
os.makedirs(output_dir, exist_ok=True)

# 텍스트 데이터 처리
# 텍스트 데이터
text = """소프트웨어 개발자, 소프트웨어 개발자, 소프트웨어 개발자, 소프트웨어 개발자,
소프트웨어 개발자, 데이터 분석가, 데이터 분석가, 데이터 분석가, 데이터 분석가, 
인공지능 연구원, 인공지능 연구원, 인공지능 연구원, 간호사, 간호사, 간호사, 간호사, 
마케팅 전문가, 마케팅 전문가, 마케팅 전문가, 마케팅 전문가, 웹 개발자, 웹 개발자, 웹 개발자, 
웹 개발자, 교사, 교사, 교사, UX/UI 디자이너, UX/UI 디자이너, UX/UI 디자이너, 의사, 의사, 의사, 
의사, 엔지니어, 엔지니어, 엔지니어, 엔지니어, 회계사, 회계사, 회계사, 변호사, 변호사, 변호사, 변호사, 
변호사, 심리학자, 심리학자, 심리학자, 항공 승무원, 항공 승무원, 항공 승무원, 요리사, 요리사, 요리사, 
경찰관, 경찰관, 경찰관, IT 컨설턴트, IT 컨설턴트, IT 컨설턴트, 건축가, 건축가, 콘텐츠 크리에이터, 콘텐츠 크리에이터, 
물리치료사, 물리치료사, 물류 관리자, 물류 관리자, 물류 관리자, 물류 관리자, 게임 개발자, 게임 개발자, 게임 개발자, 
게임 개발자, 치과 의사, 치과 의사, 치과 의사, 치과 의사, 항공 엔지니어, 항공 엔지니어, 항공 엔지니어, 항공 엔지니어, 
작가, 작가, 작가, 작가, 편집자, 편집자, 편집자, 편집자, 재무 분석가, 재무 분석가, 재무 분석가, 재무 분석가, 군인, 
군인, 군인, 군인, 물리학자, 물리학자, 물리학자, 물리학자, 상담사, 상담사, 상담사, 상담사, 보육 교사, 보육 교사, 
보육 교사, 보육 교사, 투자 은행가, 투자 은행가, 투자 은행가, 투자 은행가, 영양사, 영양사, 영양사, 영양사, 네트워크 엔지니어, 
네트워크 엔지니어, 네트워크 엔지니어, 네트워크 엔지니어, 로봇 엔지니어, 로봇 엔지니어, 로봇 엔지니어, 로봇 엔지니어, 항만 관리자, 
항만 관리자, 항만 관리자, 항만 관리자, 환경 엔지니어, 환경 엔지니어, 환경 엔지니어, 환경 엔지니어, 이벤트 플래너, 이벤트 플래너, 
이벤트 플래너, 이벤트 플래너, 3D 모델러, 3D 모델러, 3D 모델러, 3D 모델러, 바리스타, 바리스타, 바리스타, 바리스타, 미용사, 미용사, 
미용사, 미용사, AI 연구원, AI 연구원, AI 연구원, AI 연구원, 프로그래머, 프로그래머, 프로그래머, 프로그래머, 콘텐츠 매니저, 
콘텐츠 매니저, 콘텐츠 매니저, 콘텐츠 매니저, HR 관리자, HR 관리자, HR 관리자, HR 관리자, 병원 관리자, 병원 관리자, 병원 관리자, 
병원 관리자, 여행 가이드, 여행 가이드, 여행 가이드, 여행 가이드, 출판사 편집장, 출판사 편집장, 출판사 편집장, 출판사 편집장, 
성우, 성우, 성우, 성우, 메이크업 아티스트, 메이크업 아티스트, 메이크업 아티스트, 메이크업 아티스트, 스포츠 해설가, 스포츠 해설가, 
스포츠 해설가, 스포츠 해설가, 디자이너, 디자이너, 디자이너, 디자이너
"""
words = [word.strip() for word in text.split(',') if word.strip()]
unique_words, counts = np.unique(words, return_counts=True)
freq = dict(zip(unique_words, counts))

# 마스크 이미지 로드
try:
    mask_image = np.array(Image.open(mask_path))
except Exception as e:
    raise ValueError(f"마스크 이미지 로드 오류: {e}")

# 워드클라우드 생성
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='black',
    font_path=fontpath,
    mask=mask_image,
    contour_color='black',
    contour_width=1,
    colormap='prism'
).generate_from_frequencies(freq)

# 출력 및 저장
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig(output_path, bbox_inches='tight')
plt.show()
