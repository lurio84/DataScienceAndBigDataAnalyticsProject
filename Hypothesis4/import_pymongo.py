import pandas as pd
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["game_reviews_db"]              # name of the database
collection = db["clean_sample_reviews"]     # name of the collection

# read CSV
df = pd.read_csv("clean_sample.csv")

# replace NaN with None
df = df.where(pd.notnull(df), None)

# DataFrame to MongoDB
collection.insert_many(df.to_dict(orient="records"))

print("Data inserted into MongoDB successfully.")


