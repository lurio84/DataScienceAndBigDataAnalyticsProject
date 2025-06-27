import sys
from pymongo import MongoClient

if len(sys.argv) != 2:
    print("Usage: python3 import_output_to_mongo.py <output_file>")
    sys.exit(1)

output_file = sys.argv[1]

client = MongoClient("mongodb://localhost:27017")
db = client["game_reviews_db"]
collection = db["output_h1_keywords"]

# if you want to clear the collection before importing new data
collection.delete_many({"sentiment": {"$exists": True}, "keyword": {"$exists": True}, "count": {"$exists": True}})



with open(output_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            key, count_str = line.split("\t")
            sentiment, keyword = key.split("_", 1)
            count = int(count_str)

            doc = {
                "sentiment": sentiment,
                "keyword": keyword,
                "count": count,
            }
            collection.insert_one(doc)
        except Exception as e:
            print(f"❌ Error processing line: {line}\n{e}", file=sys.stderr)

print("completed importing data to MongoDB")
