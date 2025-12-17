# ============================================================
# DAY08 – TOXIC TWEETS ANALYSIS + INTERPRETABILITY
# ============================================================

# =========================
# IMPORTS
# =========================
import os
import re
import numpy as np
import pandas as pd
import kagglehub

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =========================
# 1) DOWNLOAD + LOAD DATA
# =========================
DATASET_REF = "umitka/twitter-toxic-tweets"
DATASET_PATH = kagglehub.dataset_download(DATASET_REF)

CSV_FILE = "twitter_toxic_tweets.csv"
CSV_PATH = os.path.join(DATASET_PATH, CSV_FILE)

print("DATASET PATH:", DATASET_PATH)
print("FILES:", os.listdir(DATASET_PATH))

DF = pd.read_csv(CSV_PATH)

print("\nDF SHAPE:", DF.shape)
print("DF COLUMNS:", list(DF.columns))
print("\nDF HEAD:")
print(DF.head())

TEXT_COL = "tweet"
LABEL_COL = "label"

print("\nLABEL VALUE COUNTS:")
print(DF[LABEL_COL].value_counts())

# =========================
# 2) TEXT CLEANING (PRIMARY + SECONDARY)
# =========================
def CLEAN_TEXT(TEXT: str) -> str:
    TEXT = str(TEXT).lower()

    # PRIMARY CLEANING
    TEXT = re.sub(r"http\S+|www\.\S+", " ", TEXT)
    TEXT = re.sub(r"@\w+", " ", TEXT)
    TEXT = re.sub(r"#", " ", TEXT)
    TEXT = re.sub(r"[^a-z\s']", " ", TEXT)
    TEXT = re.sub(r"\s+", " ", TEXT).strip()

    TOKENS = TEXT.split()

    # REMOVE CONTRACTION ARTIFACTS
    CONTRACTION_FRAGMENTS = {"ve", "ll", "re", "d", "m", "s", "amp"}

    # TWITTER / GENERIC NOISE WORDS (EDIT THIS LIST FREELY)
    NOISE_WORDS = {
        "rt", "via", "retweet",
        "listen", "watch", "look",
        "will", "im", "dont", "cant",
        "http", "https", "co"
    }

    CLEAN_TOKENS = [
        T for T in TOKENS
        if T not in CONTRACTION_FRAGMENTS
        and T not in NOISE_WORDS
    ]

    return " ".join(CLEAN_TOKENS)

# CREATE CLEAN COLUMN (CRITICAL – BEFORE ANY USE)
DF["CLEAN_TWEET"] = DF[TEXT_COL].apply(CLEAN_TEXT)

print("\nTEXT CLEANING EXAMPLE:")
print("RAW  :", DF[TEXT_COL].iloc[0])
print("CLEAN:", DF["CLEAN_TWEET"].iloc[0])

# =========================
# 3) TRAIN / TEST SPLIT
# =========================
X = DF["CLEAN_TWEET"]
Y = DF[LABEL_COL]

X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42,
    stratify=Y
)

print("\nTRAIN SIZE:", X_TRAIN.shape)
print("TEST SIZE :", X_TEST.shape)

# =========================
# 4) TF-IDF VECTORIZATION
# =========================
VECTORIZER = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_TRAIN_VEC = VECTORIZER.fit_transform(X_TRAIN)
X_TEST_VEC = VECTORIZER.transform(X_TEST)

print("VECTORIZED TRAIN SHAPE:", X_TRAIN_VEC.shape)

# =========================
# 5) BASE MODEL
# =========================
MODEL = LogisticRegression(max_iter=1000)
MODEL.fit(X_TRAIN_VEC, Y_TRAIN)

Y_PRED = MODEL.predict(X_TEST_VEC)
Y_PROBA = MODEL.predict_proba(X_TEST_VEC)[:, 1]

print("\nCONFUSION MATRIX:")
print(confusion_matrix(Y_TEST, Y_PRED))

print("\nCLASSIFICATION REPORT:")
print(classification_report(Y_TEST, Y_PRED, digits=3))

print("ROC-AUC:", roc_auc_score(Y_TEST, Y_PROBA))

# =========================
# 6) GLOBAL FEATURE IMPORTANCE
# =========================
FEATURE_NAMES = VECTORIZER.get_feature_names_out()
COEFS = MODEL.coef_[0]

SORTED_IDX = np.argsort(COEFS)

TOP_TOXIC = SORTED_IDX[-20:][::-1]
TOP_NON_TOXIC = SORTED_IDX[:20]

print("\nTOP WORDS PUSHING TOXIC:")
for IDX in TOP_TOXIC:
    print(f"{FEATURE_NAMES[IDX]:<25} {COEFS[IDX]:.3f}")

print("\nTOP WORDS PUSHING NON-TOXIC:")
for IDX in TOP_NON_TOXIC:
    print(f"{FEATURE_NAMES[IDX]:<25} {COEFS[IDX]:.3f}")

# =========================
# 7) WORD CLOUDS
# =========================
NON_TOXIC_TEXT = " ".join(DF[DF[LABEL_COL] == 0]["CLEAN_TWEET"])
TOXIC_TEXT = " ".join(DF[DF[LABEL_COL] == 1]["CLEAN_TWEET"])

WC_NON = WordCloud(
    width=800,
    height=400,
    background_color="white",
    max_words=200
).generate(NON_TOXIC_TEXT)

WC_TOX = WordCloud(
    width=800,
    height=400,
    background_color="white",
    max_words=200
).generate(TOXIC_TEXT)

plt.figure()
plt.imshow(WC_NON)
plt.axis("off")
plt.title("Word Cloud – Non-toxic Tweets")
plt.show()

plt.figure()
plt.imshow(WC_TOX)
plt.axis("off")
plt.title("Word Cloud – Toxic Tweets")
plt.show()

# =========================
# 8) ROC CURVE
# =========================
FPR, TPR, _ = roc_curve(Y_TEST, Y_PROBA)

plt.figure()
plt.plot(FPR, TPR)
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.show()
