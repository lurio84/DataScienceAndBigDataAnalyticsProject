#!/bin/bash

set -e  # エラーが出たらスクリプトを停止

echo "Starting MapReduce job for Bag-of-Words creation..."

# Step 1: Upload updated clean_sample.csv to HDFS
echo "Updating clean_sample.csv in HDFS..."
hdfs dfs -rm -f /user/ubuntu/reviews/clean_sample.csv
hdfs dfs -put clean_sample.csv /user/ubuntu/reviews/

# Step 2: Remove previous output directory if it exists
echo "Removing old output directory (if any)..."
hdfs dfs -rm -r -f /user/ubuntu/output_bow

# Step 3: Run the MapReduce job using Hadoop Streaming
echo "Running Hadoop Streaming job..."
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.10.0.jar \
  -input /user/ubuntu/reviews/clean_sample.csv \
  -output /user/ubuntu/output_bow \
  -mapper mapper.py \
  -reducer reducer.py \
  -file mapper.py \
  -file reducer.py \
  -file special_tokens.txt

# Step 4: Save and show the output
echo "Saving Hadoop output to output_bow.txt..."
hdfs dfs -cat /user/ubuntu/output_bow/part-00000 > output_bow.txt

echo " MapReduce job completed. Output preview:"
head output_bow.txt

