from konlpy.tag import Okt

class TokenizerWrapper:
    def __init__(self):
        self.okt = Okt()

    def tokenize(self, text):
        return self.okt.morphs(text)

# ✅ 피클링할 때 Okt 객체를 제외하고 함수만 저장
tokenizer = TokenizerWrapper()
joblib.dump(tokenizer.tokenize, "/app/project/MovieAPP/static/model/tokenizer.pkl")

print("✅ 토크나이저 함수가 성공적으로 저장되었습니다!")
