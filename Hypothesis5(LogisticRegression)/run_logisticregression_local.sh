#!/bin/bash

spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --files special_tokens.txt,output_bow.txt \
  logistic_regression.py