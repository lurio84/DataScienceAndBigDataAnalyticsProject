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



```bash
use game_reviews_db
show collections
db.clean_sample_reviews.find().limit(10).pretty()
```

