from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizerModel, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, udf, when
from pyspark.sql.types import ArrayType, StringType
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
import re

# ---------------------
# Init Spark
# ---------------------
spark = SparkSession.builder.appName("ReviewClassification").getOrCreate()

# ---------------------
# Read BoW Dictionary
# ---------------------
vocab = []

with open("output_bow.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        # Split with Comma or Tab
        if ',' in line:
            parts = line.split(',')
        elif '\t' in line:
            parts = line.split('\t')
        else:
            continue  

        if len(parts) >= 2:
            try:
                count = int(parts[1])
                if count > 5:
                    vocab.append(parts[0])
            except ValueError:
                continue  

# ---------------------
# Special Token Definition 
# ---------------------
special_tokens = []
with open("special_tokens.txt", "r", encoding="utf-8") as f:
    special_tokens = [line.strip().lower() for line in f if line.strip()]

pattern = '|'.join(map(re.escape, special_tokens))

@udf(ArrayType(StringType()))
def custom_tokenizer(text):
    text = text.lower()
    special = re.findall(pattern, text)
    text = re.sub(pattern, '', text)
    words = re.findall(r'\b\w+\b', text)
    return special + words

# ---------------------
# Preprocessing and Reading Data
# ---------------------
df = spark.read.csv("clean_sample_binary.csv", header=True, inferSchema=True)
print("Data loaded")

df_clean = df.select(col("review_text"), col("review_score")) \
             .na.drop() \
             .withColumn("label", when(col("review_score") == 1, 1).otherwise(0))

df_tokens = df_clean.withColumn("tokens", custom_tokenizer(col("review_text")))
print("Tokenization complete")

# ---------------------
# Train / Test（80%:20%）
# ---------------------
train_data, test_data = df_tokens.randomSplit([0.8, 0.2], seed=42)
print("Data split complete")

# ---------------------
# Feature map produced
# ---------------------
cv_model = CountVectorizerModel.from_vocabulary(vocab, inputCol="tokens", outputCol="rawFeatures")
idf = IDF(inputCol="rawFeatures", outputCol="features")

# ---------------------
# Logistic Regression Model
# ---------------------
lr = LogisticRegression(featuresCol="features", labelCol="label", maxIter=20)

# Making Pipeline
pipeline = Pipeline(stages=[cv_model, idf, lr])

# ---------------------
# Training
# ---------------------
print("Training started...")
model = pipeline.fit(train_data)
print("Model training complete")

# ---------------------
# Inference and Test
# ---------------------
predictions = model.transform(test_data)

# Binary Validation (ROC-AUC)
binary_evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
roc_auc = binary_evaluator.evaluate(predictions)



# Accuracy
multi_evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = multi_evaluator.evaluate(predictions)

print("Evaluation Results:")
print(f"  • ROC-AUC: {roc_auc:.4f}")
print(f"  • Accuracy: {accuracy:.4f}")

# ---------------------
#  produce output file
# ---------------------
output_file = "evaluation_and_predictions.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("Evaluation Results:\n")
    f.write(f"  • ROC-AUC: {roc_auc:.4f}\n")
    f.write(f"  • Accuracy: {accuracy:.4f}\n\n")
    
    f.write("Sample Predictions:\n")
    sample_preds = predictions.select("review_text", "label", "prediction", "probability").take(10)
    for row in sample_preds:
        # probabilityはDenseVectorなのでstrで整形
        prob_str = ', '.join([f"{p:.4f}" for p in row['probability']])
        f.write(f"Review Text: {row['review_text']}\n")
        f.write(f"Label: {row['label']}, Prediction: {row['prediction']}, Probability: [{prob_str}]\n")
        f.write("-" * 80 + "\n")

print(f"Results saved to {output_file}")

predictions.select("review_text", "label", "probability") \
           .toPandas() \
           .to_csv("logreg_predictions.csv", index=False)
spark.stop()
