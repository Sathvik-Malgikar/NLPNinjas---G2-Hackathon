import gensim
import gensim.downloader as api
from gensim.models import Phrases, LdaModel
from textblob import TextBlob
import json
import spacy

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

import summa

from sklearn.metrics.pairwise import cosine_similarity


def aspect_sentiment_analysis(text, aspect):
    sid = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)
    aspect_sentiments = []
    for sentence in sentences:
        if aspect.lower() in sentence.lower():
            sentiment_score = sid.polarity_scores(sentence)["compound"]
            aspect_sentiments.append(sentiment_score)
    if aspect_sentiments:
        aspect_sentiment = sum(aspect_sentiments) / len(aspect_sentiments)
        return aspect_sentiment
    else:
        return None


def extract_tags(sentence):
    # Load English tokenizer, tagger, parser, NER, and word vectors
    nlp = spacy.load("en_core_web_sm")

    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Extract POS tags
    tags = [(token.text, token.pos_, token.ent_type_) for token in doc]

    return tags


def extract_keywords(sentence, num_keywords=5):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)
    # Convert the list of words into a space-separated string
    text = " ".join(words)
    # Extract keywords using TextRank algorithm
    extracted_keywords = summa.keywords.keywords(text, words=num_keywords)
    # Split the extracted keywords and return them as a list
    return extracted_keywords.split('\n')


def compute_similarity(query_keywords, product_tags):
    # Vectorize the keywords and product tags
    vectorizer = TfidfVectorizer()
    keyword_vector = vectorizer.fit_transform(query_keywords)
    product_vector = vectorizer.transform(product_tags)
    # Calculate cosine similarity between the keyword vector and product vector
    similarity_score = cosine_similarity(keyword_vector, product_vector)
    return similarity_score[0][0]


def search_products(query, products_data):
    # Extract keywords from the query
    query_keywords = extract_keywords(query)
    # Initialize a dictionary to store product IDs and their similarity scores
    product_scores = {}
    # Iterate through each product in the dataset
    for product_id, product_tags in products_data.items():
        # Compute similarity score between query keywords and product tags
        similarity_score = compute_similarity(query_keywords, product_tags)
        # Store the similarity score for the product
        product_scores[product_id] = similarity_score
    # Sort products by their similarity scores in descending order
    sorted_products = sorted(product_scores.items(),
                             key=lambda x: x[1], reverse=True)
    return sorted_products


def append_to_json_file(file_path, key, value):
    # Read the existing JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Add the new key-value pair to the dictionary
    data[key] = value

    # Write the updated dictionary back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def extract_features(review_json):
    """
    Extracts feature sets from a single review in JSON format.

    Args:
        review_json: A dictionary containing the review data.

    Returns:
        A dictionary containing extracted features and sentiment.
    """
    nlp = spacy.load("en_core_web_sm")  # Load a small English spaCy model

    # Get the review text from the "love.value" field (positive aspects)
    text = review_json["attributes"]["comment_answers"]["love"]["value"]

    # Pre-process the text (optional):
    # You can add pre-processing steps like tokenization, lowercasing, and removing stop words.

    doc = nlp(text)  # Parse the text with spaCy

    # Define aspects (features) to identify
    aspects = ["ease of use", "customer support",
               "integration", "value for money"]

    # Extract features and sentiment
    features = {}
    for aspect in aspects:
        feature_sentiment = "neutral"  # Default sentiment

        # Option 1: Using keyword matching
        if any(aspect in token.text.lower() for token in doc):
            feature_sentiment = "positive"  # Update sentiment based on keyword match

        # Option 2: Using Named Entity Recognition (NER) (if trained domain-specific model)
        # entity_offsets = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "PRODUCT_FEATURE"]
        # if any(aspect in offset[0] for offset in entity_offsets):
        #   feature_sentiment = "positive"  # Update sentiment based on NER

        features[aspect] = feature_sentiment

    return features


def extract_features_textblob(review_json):
    """
    Extracts feature sets from a single review in JSON format using TextBlob.

    Args:
        review_json: A dictionary containing the review data.

    Returns:
        A dictionary containing extracted features and sentiment.
    """
    review_text = review_json["attributes"]["comment_answers"]["love"]["value"]
    blob = TextBlob(review_text)

    # Extract nouns (potential features)
    features = [noun.singularize() for noun in blob.noun_phrases]

    # Sentiment analysis (basic polarity)
    sentiment = "neutral"
    if blob.sentiment.polarity > 0:
        sentiment = "positive"
    elif blob.sentiment.polarity < 0:
        sentiment = "negative"

    return {"features": features, "sentiment": sentiment}


# def append_to_json_file_efficient(file_path, key, value):
    # # Open the JSON file in append mode
    # with open(file_path, 'r+') as file:
    #     # Move the file pointer to the end
    #     file.seek(0, 2)

    #     pos = file.tell()
    #     while pos > 0:
    #         pos -= 1
    #         file.seek(pos)
    #         if file.read(1) == '}':
    #             file.seek(pos)
    #             break

    #     # Remove one closing curly brace character if it's not the first record
    #     if pos > 0:
    #         file.truncate()
    #     # Write the new record
    #     if pos > 0:
    #         file.write(',')
    #     json.dump({key: value}, file, indent=4)
    #       # Move the file pointer backwards until it finds an opening curly brace character
    #     while True:
    #         pos = file.tell()
    #         if pos == 0:
    #             break
    #         file.seek(pos - 1)
    #         char = file.read(1)
    #         if char == '{':
    #             file.seek(pos - 1)
    #             file.truncate()
    #             break
    #         elif char.strip():  # If char is not whitespace, break the loop
    #             break
# Example usage:
if __name__ == "__main__":
    # Example usage
    # sentence = "Apple is looking at buying U.K. startup for $1 billion"
    # tags = extract_tags(sentence)
    # print(tags)

    # common_aspects= ["cost","performance","quality"]
    # sentence = "This app is of great value for cost"
    # print ( aspect_sentiment_analysis(sentence,common_aspects[0]))

    # sentence = "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence (AI) concerned with the interactions between computers and human language."
    # print ( extract_keywords(sentence,8))

    # print( compute_similarity(["perfume"],["perform"]))

    # # Example usage
    # query = "laptop with high performance"
    # products_data = {
    #     "product1": extract_keywords("laptop performance speed RAM CPU storage"),
    #     "product2": extract_keywords ("gaming laptop graphics card performance"),
    #     "product3": extract_keywords ("ultrabook lightweight battery life performance")
    # }

    # search_results = search_products(query, products_data)
    # print("Search Results:")
    # for product_id, similarity_score in search_results:
    #     print(f"Product ID: {product_id}, Similarity Score: {similarity_score}")

    file_path = 'data.json'  # Replace with your JSON file path
    product_id = 'new_product'
    tags = 'new_value'
    # with open("response.json", "r") as f:
    #     review_data = json.loads(f.read())
    # review_list = review_data["data"]

    # append_to_json_file(file_path, product_id, tags)
