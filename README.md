# G2 Review Analyzer

## API used

* Reviews List : [API Doc Link](https://data.g2.com/api/docs#reviews-list)

## Overview

This is the source code for the client review analysis & summarisation pipeline used by [G2 Website Link](https://g2.com)
Unbiased customer reviews are gathered from the above mentioned API endpoints and a database is built that contains organised information about different opinions and perspectives on our products. This is used by a query / search mechanism to help those looking to try our solutions to navigate reviews and get a picture of what we do and simplified view of various review metrics like votes & ratings.

## Implementation
The pipeline for processing reviews is built with python using NLP modules spacY, bert, gemini , nltk & yake.
Additional modules used: pandas, textblob, gensim

The frontend is a single page application built with Vite + React JS.
We have used react-svg-worldmap to plot the countrywise metrics, and react-chatbot-kit to power the chat with reviews UI.

![Architecture / Workflow](Arch.png?raw=true "Architecture / Workflow")

## Prerequisites
* PC With Conda installed.
* Network connection
* Node JS 21.2.0 (for frontend)
* Working kaggle api token

## Generating kaggle API token
* Visit kaggle.com and create an account
* In account settings, scroll down to API -> Create New Token
* Place the downloaded kaggle.json in C:/Users/{your_username}/.kaggle/
* Proceed with Cloning


## Commands (How to run).

To clone this repository:
```
git clone https://github.com/Sathvik-Malgikar/NLPNinjas---G2-Hackathon.git
cd NLPNinjas---G2-Hackathon
```

To setup environment with all required dependencies for processing reviews:
```
conda env create -f environment.yml
conda activate nlpninjas
```
This will make a new conda environement called 'nlpninjas' and make it active.



Use this command to serve a local flask development server for serving generated info to at API endpoints:
```
python server.py
```
Wait for it to display "Running on http://127.0.0.1:5000/"

Now, at http://127.0.0.1:5000/ the following endpoints should be accessible:

* /aggregates/average_secondary_metrics
* /aggregates/votes_data
* /aggregates/regionwise_rating
* /keyword-inferences
* /aggregates/aspect-keywords
* /aggregates/polarity-keywords
* /search/similar-docs
* /rag/query
* /rag/get-results
* /filter-reviews

Open a new terminal from root directory to serve a local frontend.
Use these commands to quickly install all dependencies for a local running version of website.
```
cd frontend
npm i
```
The /frontend can be run as development server using 
```
npm run dev
```
The frontend can be accessed at http://localhost:5173/

Search G2 on Homepage's Searchbox to get started!

[Optional]
Open a new terminal to run NLP locally.
Run the following commands to re generate processed reviews and aggregate metrics. This will run NLP pipeline locally and takes a long time:
```
python process_reviews.py
```
This will generate several json files and CSV files with aggregate info in /insight_collection/outputs .

## How are reviews aggregated?

* Country-wise star-rating
* Finding mean of metrics given in secondary comments
* Finding keywords for the different love and hate comments given in reviews and indexing them to query through suggest relevant reviews to user by finding similarity between query and these tags.
* These keywords are also run through sentiment analysis. After eliminating duplicate ones, top 10 adjectives from both these keywords categories are selected. These represent the Pros & Cons of product
* These keywords are fed to gemini API to get additional info on what the top customer expectations are.
* Statistics corresponding to votes given in reviews
* Getting polarity scores corresponding to the common aspects which users look for, like value-for-money, ease-of-use, performance, scalability and using this to fetch suitable reviews and display
* There is a search reviews through filter mechanism where user can find and read relevant reviews by selecting some of these aspects. Based on polarity scores reviews are most suited for the tags selected are displayed.

## Links

Some useful links that might help you:

- [API Doc Link](https://data.g2.com/api/docs#reviews-list)


## Source Code sitemap
```
/NLP/data_collection                Contains notebook used to parse through API and scrape all the reviews, store them into a CSV (reviews.csv) for further processing
/NLP/insight_collection           Contains individual parts responsible for different metrics and aggregate analysis (average secondary comments metrics , keywords , regionwise ratings,etc)
/NLP/insight_collection/process_reviews.py           This is the mainfile that reads reviews.csv and uses above mentioned review components then dumps all generated results into several json files in /insight_collection/outputs
NLP/insight_collection/outputs   Contains all the insights gathered from the processing to be used by flask backend to serve responses to users
/frontend                    Contains the Web UI & charts Single Page Application built using React JS.
server.py                    Contains python flask code responsible for routing and backend logic 
environment.yml            Contains names and versions of different python modules and packages used.  
```
