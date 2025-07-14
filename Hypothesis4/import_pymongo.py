import pandas as pd
from pymongo import MongoClient
import sys

# Check if the script is run with the --clean option
clean_mode = "--clean" in sys.argv

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["game_reviews_db"]              # database name
collection = db["clean_sample_reviews"]     # collection name

# --clean option was selected
if clean_mode:
    print("--clean option was selected...deleting existing data in 'clean_sample_reviews' collection.")
    collection.delete_many({})
    print("Existing data deleted.")

# CSVを読み込む
df = pd.read_csv("clean_sample.csv")

# 必要に応じて、NaNをNoneに変換（MongoDBではnull相当）
df = df.where(pd.notnull(df), None)

# DataFrameを辞書のリストに変換してMongoDBへ一括挿入
collection.insert_many(df.to_dict(orient="records"))

print(f"データをMongoDBにインポートしました。({len(df)}件)")
