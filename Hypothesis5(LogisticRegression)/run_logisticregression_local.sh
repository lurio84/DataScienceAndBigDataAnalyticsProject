#!/bin/bash

spark-submit \
  --master local[*] \
  --deploy-mode cluster \
  --files special_tokens.txt,output_bow.txt \
  logistic_regression.py