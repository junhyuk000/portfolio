from konlpy.tag import Okt
import joblib

class TokenizerWrapper:
    def __init__(self):
        self.okt = Okt()
    
    def tokenize(self, text):
        return self.okt.morphs(text)

# ✅ 전역적으로 사용할 객체 생성
tokenizer = TokenizerWrapper()

# ✅ 이 파일이 실행될 때만 모델을 새로 저장
if __name__ == "__main__":
    joblib.dump(tokenizer, "tokenizer.pkl")
