# DataScienceAndBigDataAnalyticsProject
---
## Setup for MongoDB server
mongo is installed, so you can use *pymongo_importdata.py*
this program import "clean_sample.csv" into mongoDB

when you have "clean_sample.csv" at current directory,
```bash
python3 pymongo_importdata.py
```

```bash
mongo
show collections
db.clean_sample_reviews.find().limit(10).pretty()
```

```plaintext
MongoDB shell version v3.6.8
connecting to: mongodb://127.0.0.1:27017
Implicit session: session { "id" : UUID("a3ba028f-a18e-483c-8c64-c9574d92e3cc") }
MongoDB server version: 3.6.8
Welcome to the MongoDB shell.

clean_sample_reviews

{
	"_id" : ObjectId("685f144f95ab191fc705cd6f"),
	"app_id" : 10,
	"app_name" : "Name of the game",
	"review_text" : "Good Game.",
	"review_score" : 1,
	"review_votes" : 0
}
```


## hypothesis
### H1

if you have results "output_h1.txt", you can make it into MongoDB:
```bash
python3 import_output_to_mongo.py output_H1.py
mongo
use game_reviews_db
db.output_h1_keywords.find().pretty()
```

The data is saved as follows:
```plaintext
{
        "_id" : ObjectId("685f1f3931447ec680419a4c"),
        "sentiment" : "neg",
        "keyword" : "fun",
        "count" : 1001
}
```

### H2

### H3

### H4

### H5 Losistic Regression
This model was implemented with `Pyspark`. 

Hypothesis: with this model, `review_score` can be predicted with high percentage. This model can repair the `review_score` when this data is not collected.

Evaluation Results:
  • ROC-AUC: 0.8482
  • Accuracy: 0.8732

Sample Predictions: (Prediction: 1.0 = Positive, 0.0 = Negative. [P(pos),P(neg)])
Review Text:   
Label: 1, Prediction: 1.0, Probability: [0.0828, 0.9172]
--------------------------------------------------------------------------------
Review Text:       property
Label: 1, Prediction: 1.0, Probability: [0.0118, 0.9882]
--------------------------------------------------------------------------------
Review Text:     back in my day!
Label: 1, Prediction: 1.0, Probability: [0.0390, 0.9610]
--------------------------------------------------------------------------------
Review Text:    pluses :  nostalgia, simple gameplay.    minuses :  graphics of ten-year prescription.    game counter strike is recommended who missed game clubs and the school and student's days spent to us! 
Label: 1, Prediction: 0.0, Probability: [0.9043, 0.0957]
--------------------------------------------------------------------------------
Review Text:   &lt;3 love it *__*
Label: 1, Prediction: 1.0, Probability: [0.0423, 0.9577]
--------------------------------------------------------------------------------
Review Text:   .
Label: 1, Prediction: 1.0, Probability: [0.0828, 0.9172]
--------------------------------------------------------------------------------
Review Text:   ...
Label: 1, Prediction: 1.0, Probability: [0.0828, 0.9172]
--------------------------------------------------------------------------------
Review Text:   10/10. that's all i need to say.
Label: 1, Prediction: 1.0, Probability: [0.0058, 0.9942]
--------------------------------------------------------------------------------
Review Text:   9/10
Label: 1, Prediction: 1.0, Probability: [0.0391, 0.9609]
--------------------------------------------------------------------------------
Review Text:   :)
Label: 1, Prediction: 1.0, Probability: [0.0828, 0.9172]
--------------------------------------------------------------------------------

#### How to run 
please make sure that there's  `clean_sample.csv` in /user/ubuntu/reviews/
```
./run_mapreduce.sh
./run_logisticregression_local.sh
```
If there is `output_bow.txt`, `./run_logisticregression_local.sh` will work properly