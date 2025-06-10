from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover
from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, StringType
import re

# Spark起動
spark = SparkSession.builder.appName("ReviewClassification").getOrCreate()

# BoW辞書の読み込み
vocab = [line.split('\t')[0] for line in open("output_bow.txt") if int(line.split('\t')[1]) > 5]

# UDFで特殊単語も含めたトークナイザーを作成
special_tokens = ["10/10", "piece of ****", "not recommended"]
pattern = '|'.join(map(re.escape, special_tokens))

@udf(ArrayType(StringType()))
def custom_tokenizer(text):
    text = text.lower()
    special = re.findall(pattern, text)
    text = re.sub(pattern, '', text)
    words = re.findall(r'\b\w+\b', text)
    return special + words

# データ読み込み
df = spark.read.csv("hdfs:///path/to/reviews.csv", header=True, inferSchema=True)

# データ前処理
df_clean = df.select(col("review_text"), col("review_score").alias("label")) \
             .na.drop()

df_tokens = df_clean.withColumn("tokens", custom_tokenizer(col("review_text")))

# 特徴量生成
cv = CountVectorizer(inputCol="tokens", outputCol="rawFeatures", vocabSize=5000, minDF=5, vocabulary=vocab)
idf = IDF(inputCol="rawFeatures", outputCol="features")

# モデル
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=20)

# パイプライン
pipeline = Pipeline(stages=[cv, idf, lr])

# 学習
model = pipeline.fit(df_tokens)

# 推論（例）
predictions = model.transform(df_tokens)
predictions.select("review_text", "label", "prediction").show(10)
