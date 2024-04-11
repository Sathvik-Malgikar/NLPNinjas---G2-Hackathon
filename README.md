# G2 Review Analyzer

## API used

* Reviews List : [API Doc Link](https://data.g2.com/api/docs#reviews-list)

## Overview

This is the source code for the client review analysis & summarisation pipeline used by [G2 Website Link](https://g2.com)
Unbiased customer reviews are gathered from the above mentioned API endpoints and a database is built that contains organised information about different opinions and perspectives on our products. This is used by a query / search mechanism to help those looking to try our solutions to navigate reviews and get a picture of what we do and simplified view of various review metrics like votes & ratings.

## Implementation
The pipeline for processing reviews is built with python using NLP modules spacY , nltk & yake.
Additional modules used: pandas, textblob, gensim
Checkout requirements.txt for more info!

The frontend is a single page application built with React JS.
We have used chart JS to plot the metrics and make UI aesthetics.
The found in /frontend can be run as development server using 
```
npm start
```

## Commands.
This will setup required dependencies for processing reviews, and installs NLP bundles.
```
pip install -r requirements.txt
```
Use the following command to initiate review processing. This will generate several json files and CSV files with aggregate info in /insight_collection/outputs 
```
python process_reviews.py
```

Use this command to serve a local flask development server for serving generated info to at API endpoints.
```
python server.py
```

Now, at http://127.0.0.1:5000/ the following endpoints should be accesible:

/aggregates/average_secondary_metrics
/aggregates/votes_data
/aggregates/regionwise_rating

## How are reviews aggregated?

* Country-wise star-rating
* Finding mean of metrics given in secondary comments
* Finding keywords for the different love and hate comments given in reviews and indexing them to query through suggest relevant reviews to user by finding similarity between query and these tags.
* Statistics corresponding to votes given in reviews
* Getting polarity scores corresponding to the common aspects which users look for, like value-for-money, ease-of-use, performance, scalability and using this to fetch suitable reviews and display


## Links

Some useful links that might help you:

- [API Doc Link](https://data.g2.com/api/docs#reviews-list)


## Source Code sitemap
```
/NLP/data_collection                Contains notebook used to parse through API and scrape all the reviews, store them into a CSV (reviews.csv) for further processing
/insight_collection           Contains individual parts responsible for different metrics and aggregate analysis (average secondary comments metrics , keywords , regionwise ratings,etc)
process_reviews.py           This is the mainfile that reads reviews.csv and uses above mentioned review components then dumps all generated results into several json files in /insight_collection/outputs
/insight_collection/outputs   Contains all the insights gathered from the processing to be used by flask backend to serve responses to users
/frontend                    Contains the Web UI & charts Single Page Application built using React JS.
server.py                    Contains python flask code responsible for routing and backend logic 
requirements.txt             Contains names and versions of different python modules and packages used.  
```
