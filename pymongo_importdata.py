import pandas as pd
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["game_reviews_db"]              # name of the database
collection = db["clean_sample_reviews"]     # name of the collection

# read CSV file
df = pd.read_csv("clean_sample.csv")

# replace NaN values with None for MongoDB compatibility 
df = df.where(pd.notnull(df), None)

# insert data into MongoDB collection
collection.insert_many(df.to_dict(orient="records"))

print("imported data successfully.")