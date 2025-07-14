import pandas as pd
from textblob import TextBlob
from sklearn.metrics import accuracy_score, roc_auc_score

# ---------------------
# read data
# ---------------------
df = pd.read_csv("clean_sample_binary.csv")
df = df.dropna(subset=["review_text", "review_score"])

# ---------------------
# label column creation
# ---------------------
df["label"] = df["review_score"].apply(lambda x: 1 if x == 1 else 0)

# ---------------------
# TextBlob sentiment analysis
# ---------------------
def get_polarity(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0.0  # fallback: neutral

df["polarity"] = df["review_text"].apply(get_polarity)
df["textblob_prediction"] = df["polarity"].apply(lambda p: 1 if p > 0 else 0)

# ---------------------
# 精度とROC-AUCの計算
# ---------------------
accuracy = accuracy_score(df["label"], df["textblob_prediction"])
try:
    roc_auc = roc_auc_score(df["label"], df["polarity"])
except ValueError as e:
    roc_auc = float('nan')
    print("ROC-AUC could not be computed:", e)

# ---------------------
# 結果表示
# ---------------------
print(f"TextBlob Accuracy: {accuracy:.4f}")
print(f"TextBlob ROC-AUC : {roc_auc:.4f}")
