import pandas as pd
import json

from regionwise import extract_country_name, extract_star_rating
from getloveandhateinfo import get_love_and_hate_comment_keywords
from vote_counter import extract_vote_counts, getvotesinfo
from average_secondary_metrics import extract_secondary_comments_value, get_avg_values
from tags_extract import extract_features, extract_features_textblob, extract_features_wrapper


def write_output(filename, data):
    with open("./outputs/"+filename, 'w') as file:
        json.dump(data, file, indent=4)

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_keywords(column_value,review_id):
    try:
        
        data = eval(column_value)
        love_keywords = data["love_keywords"]
        hate_keywords = data["hate_keywords"]
        
        return ({"review_id" : review_id, "love_keywords" : love_keywords,"hate_keywords" : hate_keywords})
    except Exception as e:
        print(e)
        print("keyword extraction failed!")

def merge_keywords_set():
    keywords_set_1 = read_json_from_file("./outputs/weighted_keywords.json")
    keywords_set_2 = pd.read_csv('./outputs/reviews_bert_keywords.csv')
    
    keywords_set_2 = keywords_set_2.apply(lambda row: read_keywords(row['attributes'], row['id']), axis=1)
    keywords_set_2 = keywords_set_2.reset_index().to_dict(orient='records')
    
    augdata = {}
    for ele in keywords_set_2:
        # print(ele[0])
        augdata[ele[0]["review_id"]] = {"love_keywords": ele[0]["love_keywords"], "hate_keywords": ele[0]["hate_keywords"]}
    
    keywords_set_2 = augdata
    write_output("weighted_keywords_bert.json",keywords_set_2)
    
    combined_set = {}
    # MERGE SETS NOW
    # print ("7098976" in keywords_set_1)
    # print (7098976 in keywords_set_2)
    review_ids =  set.union(set(keywords_set_1.keys()),set(map(str,keywords_set_2.keys()))) 
    for r_id in review_ids:
        temp_l_words=[]
        temp_h_words=[]
        if r_id in keywords_set_1:
            temp_l_words.extend(keywords_set_1[r_id]["love_keywords"])
            temp_h_words.extend(keywords_set_1[r_id]["hate_keywords"])
            
        if int(r_id) in keywords_set_2:
            temp_l_words.extend(keywords_set_2[int(r_id)]["love_keywords"])
            temp_h_words.extend(keywords_set_2[int(r_id)]["hate_keywords"])
        
        combined_set[r_id] = {"love_keywords": temp_l_words, "hate_keywords": temp_h_words}
    
    write_output("combined_keywords.json",combined_set)
    
    

if __name__ == "__main__":
    merge_keywords_set()
    exit()
    df = pd.read_csv('./outputs/reviews.csv')
    # output = {}

    # # votes aggregation

    # df['attributes'].apply(extract_vote_counts)
    # totalvotes, upvotes, downvotes = getvotesinfo()

    # data = {
    #     "totalvotes": totalvotes,
    #     "upvotes": upvotes,
    #     "downvotes": downvotes,

    # }
    # write_output("votes_aggregation.json", data)

    # # regionwise star rating

    # # Apply the function to extract the rating value
    # df['country_name'] = df['attributes'].apply(extract_country_name)
    # df['star_rating'] = df['attributes'].apply(extract_star_rating)

    # # Group by 'country' column and calculate average of 'star_rating'
    # avg_ratings = df.groupby('country_name')['star_rating'].mean()
    # data = avg_ratings.reset_index().to_dict(orient='records')
    # aug_data = {}
    # for ele in data:
    #     aug_data[ele["country_name"]] = ele["star_rating"]

    # data = aug_data
    # write_output("regionwise_rating.json", data)

    # # love ane hate keywords
    # weighted_keywords = df.apply(lambda row: get_love_and_hate_comment_keywords(
    #     row['attributes'], row['id']), axis=1)
    # data = weighted_keywords.reset_index().to_dict(orient='records')

    # augdata = {}
    # for ele in data:
    #     value = ele[0]
    #     if value is None:
    #         print("skipped")
    #         continue
    #     augdata[value["review_id"]] = {
    #         "love_keywords": value["love_keywords"], "hate_keywords": value["hate_keywords"]}
    # data = augdata
    # write_output("weighted_keywords.json", data)

    # # average_secondary_metrics
    # df['attributes'].apply(extract_secondary_comments_value)
    # data = get_avg_values()

    # write_output("average_secondary_metrics.json", data)

    # extracted_features_from_review = df['attributes'].apply(
    #     lambda x: extract_features_wrapper(x, extract_features))
    extracted_features_textblob_from_review = df['attributes'].apply(
        lambda x: extract_features_wrapper(x, extract_features_textblob))
    # review_features = {"review_data": extracted_features_from_review.tolist()}
    review_features_textblob = {
        "review_data": extracted_features_textblob_from_review.tolist()}
   # write_output("extracted_features_spacy.json", review_features)
    write_output("extracted_features_textblob_polarity.json",
                 review_features_textblob)
