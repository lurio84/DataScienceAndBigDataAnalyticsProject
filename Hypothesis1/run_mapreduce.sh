#!/bin/bash

#start-dfs.sh
#start-yarn.sh

echo "🚀 Starting MapReduce job for Hypothesis 1 analysis..."

# Step 1: Upload updated clean_sample.csv to HDFS
echo "📤 Updating clean_sample.csv in HDFS..."
hdfs dfs -rm /user/ubuntu/reviews/clean_sample.csv
hdfs dfs -put clean_sample.csv /user/ubuntu/reviews/

# Step 2: Remove previous output directory if it exists
echo "🧹 Removing old output directory (if any)..."
hdfs dfs -rm -r /user/ubuntu/output_h1

# Step 3: Run the MapReduce job using Hadoop Streaming
echo "📦 Running Hadoop Streaming job..."
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.10.0.jar \
  -input /user/ubuntu/reviews/clean_sample.csv \
  -output /user/ubuntu/output_h1 \
  -mapper mapper.py \
  -reducer reducer.py \
  -file mapper.py \
  -file reducer.py

# Step 4: Save and show the output
echo "📄 Saving Hadoop output to output_h1.txt..."
hdfs dfs -cat /user/ubuntu/output_h1/part-00000 > output_h1.txt

echo "📄 MapReduce job completed. Output preview:"
head output_h1.txt
