import joblib
from tokenizer import tokenizer  # ✅ TokenizerWrapper 불러오기

# ✅ 모델 훈련 후 저장하는 부분
tfidf_vectorizer = ...  # TF-IDF 모델 생성 코드
text_mining_model = ...  # 감성 분석 모델 훈련 코드

# ✅ 모델과 함께 tokenizer 저장
joblib.dump(tfidf_vectorizer, "/app/project/MovieAPP/static/model/tfidf.pkl")
joblib.dump(text_mining_model, "/app/project/MovieAPP/static/model/SA_lr_best.pkl")
joblib.dump(tokenizer, "/app/project/MovieAPP/static/model/tokenizer.pkl")
