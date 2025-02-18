from konlpy.tag import Okt

class TokenizerWrapper:
    def __init__(self):
        self.okt = Okt()
    
    def tokenize(self, text):
        return self.okt.morphs(text)

# ✅ 전역적으로 사용할 객체 생성
tokenizer = TokenizerWrapper()
