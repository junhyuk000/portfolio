from konlpy.tag import Okt

# Okt 토크나이저 정의
okt = Okt()

# 문장을 토큰화하기 위한 커스텀 토크나이저
def okt_tokenizer(text):
    return okt.morphs(text)