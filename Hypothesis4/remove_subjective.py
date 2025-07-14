from pymongo import MongoClient
from textblob import TextBlob

# MongoDB 接続
client = MongoClient("mongodb://localhost:27017")
db = client["game_reviews_db"]
input_collection = db["remove_meaningless_reviews"]
output_collection = db["objective_reviews"]

# 客観的レビューの抽出
objective_reviews = []
for doc in input_collection.find():
    review_id = doc["_id"]
    if output_collection.find_one({"_id": review_id}):
        continue  # 既に登録済みならスキップ

    review_text = doc.get("review_text", "")
    subjectivity = TextBlob(review_text).sentiment.subjectivity

    if subjectivity < 0.3:
        doc["subjectivity"] = subjectivity
        objective_reviews.append(doc)

# 保存
if objective_reviews:
    output_collection.insert_many(objective_reviews)

print("Objective filtering is executed. Saved in 'objective_reviews'.")
print("If you want to see the results, execute below:")
print("db.objective_reviews.find().pretty()")
print(f"Total objective reviews: {len(objective_reviews)}")
print("\n--- Sample of Objective Reviews ---")
for r in objective_reviews[:5]:
    print(f"- {r['review_text']} (subjectivity={r['subjectivity']:.2f})")
