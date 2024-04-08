import spacy

from nltk.sentiment import SentimentIntensityAnalyzer

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
    tags = [(token.text, token.pos_,token.ent_type_) for token in doc]
    
    return tags

# Example usage
sentence = "Apple is looking at buying U.K. startup for $1 billion"
tags = extract_tags(sentence)
print(tags)
