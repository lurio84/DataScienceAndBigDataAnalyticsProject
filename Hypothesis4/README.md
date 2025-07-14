# H4 

Import pymongo. You need to have `clean_sample_reviews` in your current directory.
```
python import_pymongo.py
```
Next, execute filtering with MongoDB query and `review_votes==1`.
```
python remove_meaningless.py
```
Third, execute TextBlob subjectiveness filtering.
```
python remove_subjective.py
```
Finally, execute TF-IDF for each game, each good/bad respectively.
```
python spark_PN_TF-IDF.py
```
You will get the picture of the 