import sys
import re
from pymongo import MongoClient

# MongoDB接続
client = MongoClient("mongodb://localhost:27017")
print("Connected to Database...")
db = client["game_reviews_db"]
input_collection = db["clean_sample_reviews"]
output_collection = db["remove_meaningless_reviews"]
print("Start Processing...")
# 出力コレクション初期化
if "--clear" in sys.argv:
    print("Clearing the output collection...")
    output_collection.delete_many({})

# 無意味なレビュー除去フィルタ
filtered_cursor = input_collection.find({
    "$and": [
        { "review_votes": 1 },
        { "review_text": { "$not": re.compile(r"^\s*$") } }, # null comment
        { "review_text": { "$not": re.compile(r"^\s*[\d\s/]+\s*$") } },  #only number
        { "review_text": { "$not": re.compile(r"(:\)|:\(|:D|XD|xD|;\)|:\'\(|\^\^|:3)") } }, #only facial exp
        {
            "$expr": {
                "$gt": [
                    { "$size": { "$split": [ { "$ifNull": ["$review_text", ""] }, " "] } },
                    3  # words > 3
                ]
            }
        }
    ]
})

# カーソル → リスト変換
filtered_reviews = list(filtered_cursor)

# MongoDBに保存
if filtered_reviews:
    output_collection.insert_many(filtered_reviews)

# 出力メッセージ
print("Filtering is executed. Saved in 'remove_meaningless_reviews'.")
print(f"Total filtered reviews: {len(filtered_reviews)}")
print("If you want to see the results, execute below:")
print("db.remove_meaningless_reviews.find().limit(5)")

# 最初の数件を表示
print("\n=== Sample Filtered Reviews ===")
for i, doc in enumerate(filtered_reviews[:5]):
    print(f"{i+1}. {doc.get('review_text', '[No Text]')}")
