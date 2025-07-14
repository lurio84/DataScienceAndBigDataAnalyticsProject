import pandas as pd
from pymongo import MongoClient

# MongoDB接続
client = MongoClient("mongodb://localhost:27017/")
db = client["game_reviews_db"]              # データベース名
collection = db["clean_sample_reviews"]     # コレクション名

# CSVを読み込む
df = pd.read_csv("clean_sample.csv")

# 必要に応じて、NaNをNoneに変換（MongoDBではnull相当）
df = df.where(pd.notnull(df), None)

# DataFrameを辞書のリストに変換してMongoDBへ一括挿入
collection.insert_many(df.to_dict(orient="records"))

print("データをMongoDBにインポートしました。")
