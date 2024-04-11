from tags_extract import extract_keywords

import pandas as pd

# Read CSV file into a DataFrame
import json

def get_love_and_hate_comment_keywords(column_value,review_id):
    try:
        # print(column_value)
        love_text= ""
        hate_text = ""
        data = eval(column_value)
        love_text = data["comment_answers"]["love"]["value"]
        hate_text = data["comment_answers"]["hate"]["value"]
        
        return ({"review_id" : review_id, "love_keywords" : extract_keywords(love_text),"hate_keywords" : extract_keywords(hate_text)})
    except Exception as e:
        print(e)
        print("keyword extraction failed!")

    


if __name__=="__main__":

    df = pd.read_csv('reviews.csv')
    
    df['weighted_keywords'] = df.apply(lambda row: get_love_and_hate_comment_keywords(row['attributes'], row['id']), axis=1)
    
    df.to_csv('output_file.csv', index=False)