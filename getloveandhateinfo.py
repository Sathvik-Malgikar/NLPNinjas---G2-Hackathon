from tags_extract import extract_keywords

import pandas as pd

# Read CSV file into a DataFrame
df = pd.read_csv('reviews.csv')

import json

def get_love_and_hate_comment_keywords(column_value):
    try:
        # print(column_value)
        love_text= ""
        hate_text = ""
        data = eval(column_value)
        love_text = data["comment_answers"]["love"]["value"]
        hate_text = data["comment_answers"]["hate"]["value"]
        
        return json.dumps({"love_keywords" : extract_keywords(love_text),"hate_keywords" : extract_keywords(hate_text)})
    except Exception as e:
        print(e)
        print("keyword extraction failed!")

df['weighted_keywords'] = df['attributes'].apply(get_love_and_hate_comment_keywords)

df.to_csv('output_file.csv', index=False)