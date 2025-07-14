from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, IDF
from pyspark.ml.feature import CountVectorizer, IDF
from pymongo import MongoClient
import matplotlib.pyplot as plt
import os
import string
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.ml.linalg import DenseVector
import numpy as np

# exhibit matplotlib
def plot_word_table(app_name, label, word_scores, save_dir="table"):
    emoji = "👍" if label == "positive" else "👎"
    label_title = f"{emoji} {label.capitalize()} Reviews - {app_name}"
    os.makedirs(save_dir, exist_ok=True)

    fig, ax = plt.subplots()
    ax.set_axis_off()

    table_data = [["Rank", "Word", "TF-IDF Score"]]
    for i, (word, score) in enumerate(word_scores, 1):
        table_data.append([str(i), word, f"{score:.1f}"])

    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(12)

    plt.title(label_title, fontsize=14, weight='bold')
    plt.tight_layout()

    safe_app_name = app_name.replace(" ", "_").replace("/", "_")
    filename = f"{label}_{safe_app_name}.png"
    filepath = os.path.join(save_dir, filename)
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filepath}")

# get data from MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["game_reviews_db"]
collection = db["objective_reviews"]

raw_data = list(collection.find({}, {"app_name": 1, "review_text": 1, "review_score": 1}))
print("✅ Connected and data fetched from MongoDB")

# Spark session setup
spark = SparkSession.builder.appName("TFIDFReviews").getOrCreate()

# PySpark schema definition
schema = StructType([
    StructField("app_name", StringType(), True),
    StructField("review_text", StringType(), True),
    StructField("review_score", IntegerType(), True)
])

# PySpark DataFrame creation
filtered_data = [row for row in raw_data if row.get("app_name") and row.get("review_text") and row.get("review_score") in [-1, 1]]
rdd = spark.sparkContext.parallelize([(row["app_name"], row["review_text"], row["review_score"]) for row in filtered_data])
df = spark.createDataFrame(rdd, schema)

# DataFrame preprocessing
df = df.withColumn("label", df.review_score)

# Tokenize & Stopwords
tokenizer = Tokenizer(inputCol="review_text", outputCol="words")
df_words = tokenizer.transform(df)

remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
df_filtered = remover.transform(df_words)

# learning CountVectorizer
cv = CountVectorizer(inputCol="filtered_words", outputCol="rawFeatures", vocabSize=10000)
cv_model = cv.fit(df_filtered)
featurizedData = cv_model.transform(df_filtered)

# Calculate IDF
idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)

# Extract vocabulary
vocabulary = cv_model.vocabulary  # index -> 単語
grouped_data = rescaledData.select("app_name", "label", "features").rdd\
    .map(lambda row: ((row["app_name"], row["label"]), row["features"]))\
    .groupByKey()

top_n = 5
for (app_name, label), vectors in grouped_data.collect():
    vector_sum = np.sum([v.toArray() for v in vectors], axis=0)
    top_indices = vector_sum.argsort()[::-1][:top_n]
    top_words = [(vocabulary[i], vector_sum[i]) for i in top_indices]

    print(f"\n🎮 {app_name} - {'Positive' if label == 1 else 'Negative'}")
    for word, score in top_words:
        print(f"    - {word}: {score:.1f}")

    plot_word_table(app_name, "positive" if label == 1 else "negative", top_words)

