from konlpy.tag import Okt
import joblib

class TokenizerWrapper:
    def __init__(self):
        self.okt = Okt()

    def tokenize(self, text):
        return self.okt.morphs(text)

# 객체 생성
tokenizer = TokenizerWrapper()

# ✅ `tokenize` 메서드만 저장 (Okt 객체는 피클링 불가)
joblib.dump(tokenizer.tokenize, "/app/project/MovieAPP/static/model/tokenizer.pkl")
print("✅ 토크나이저 함수가 성공적으로 저장되었습니다!")
