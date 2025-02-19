import numpy as np
import pandas as pd
import re
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import joblib
import os
# NSMC 데이터셋 로드 및 전처리
nsmc_train_df = pd.read_csv(
    'https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt', sep='\t', encoding='utf8', engine='python'
)
nsmc_test_df = pd.read_csv(
    'https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt', sep='\t', encoding='utf8', engine='python'
)

nsmc_train_df = nsmc_train_df[nsmc_train_df['document'].notnull()]
nsmc_train_df['document'] = nsmc_train_df['document'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ가-힣]+', '', x))

nsmc_test_df = nsmc_test_df[nsmc_test_df['document'].notnull()]
nsmc_test_df['document'] = nsmc_test_df['document'].apply(lambda x: re.sub(r'[^ ㄱ-ㅣ가-힣]+', '', x))

# Okt 토크나이저 정의
okt = Okt()

def okt_tokenizer(text):
    return okt.morphs(text)

# 🔹 `globals()`에 등록하여 joblib이 로드할 때 찾을 수 있도록 설정
globals()["okt_tokenizer"] = okt_tokenizer

# TF-IDF 벡터 변환기 생성 및 학습
tfidf = TfidfVectorizer(tokenizer=okt_tokenizer, ngram_range=(1, 2), min_df=3, max_df=0.9)
tfidf.fit(nsmc_train_df['document'])

# TF-IDF 변환
nsmc_train_tfidf = tfidf.transform(nsmc_train_df['document'])

# 로지스틱 회귀 모델 학습
model = LogisticRegression(random_state=0)
model.fit(nsmc_train_tfidf, nsmc_train_df['label'])

# 그리드 서치
params = {'C': [1, 3, 3.5, 4, 4.5, 5]}
SA_lr_grid_cv = GridSearchCV(model, param_grid=params, cv=3, scoring='accuracy', verbose=1)
SA_lr_grid_cv.fit(nsmc_train_tfidf, nsmc_train_df['label'])

print(SA_lr_grid_cv.best_params_, round(SA_lr_grid_cv.best_score_, 4))
SA_lr_best = SA_lr_grid_cv.best_estimator_

# 모델 저장 디렉토리 설정
MODEL_DIR = "/app/project/MovieAPP/static/model"

# 모델 저장
joblib.dump(tfidf, os.path.join(MODEL_DIR, 'tfidf.pkl'))
joblib.dump(SA_lr_best, os.path.join(MODEL_DIR, 'SA_lr_best.pkl'))

print("✅ 모델 저장 완료!")
