import pandas as pd
import json

from regionwise import extract_country_name, extract_star_rating
from getloveandhateinfo import get_love_and_hate_comment_keywords
from vote_counter import extract_vote_counts, getvotesinfo
from average_secondary_metrics import extract_secondary_comments_value, get_avg_values
from tags_extract import extract_features, extract_features_textblob, extract_features_wrapper
from aspect_analysis import init_sentiment_model, get_aspect_analysis_all_aspects_per_field


def write_output(filename, data):
    with open("./outputs/"+filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":

    df = pd.read_csv('./outputs/reviews.csv')
    output = {}

    # votes aggregation

    df['attributes'].apply(extract_vote_counts)
    totalvotes, upvotes, downvotes = getvotesinfo()

    data = {
        "totalvotes": totalvotes,
        "upvotes": upvotes,
        "downvotes": downvotes,

    }
    write_output("votes_aggregation.json", data)

    # regionwise star rating

    # Apply the function to extract the rating value
    df['country_name'] = df['attributes'].apply(extract_country_name)
    df['star_rating'] = df['attributes'].apply(extract_star_rating)

    # Group by 'country' column and calculate average of 'star_rating'
    avg_ratings = df.groupby('country_name')['star_rating'].mean()
    data = avg_ratings.reset_index().to_dict(orient='records')
    aug_data = {}
    for ele in data:
        aug_data[ele["country_name"]] = ele["star_rating"]

    data = aug_data
    write_output("regionwise_rating.json", data)

    # love ane hate keywords
    weighted_keywords = df.apply(lambda row: get_love_and_hate_comment_keywords(
        row['attributes'], row['id']), axis=1)
    data = weighted_keywords.reset_index().to_dict(orient='records')

    augdata = {}
    for ele in data:
        value = ele[0]
        if value is None:
            print("skipped")
            continue
        augdata[value["review_id"]] = {
            "love_keywords": value["love_keywords"], "hate_keywords": value["hate_keywords"]}
    data = augdata
    write_output("weighted_keywords_yake.json", data)

    # average_secondary_metrics
    df['attributes'].apply(extract_secondary_comments_value)
    data = get_avg_values()

    write_output("average_secondary_metrics.json", data)

    extracted_features_from_review = df['attributes'].apply(
        lambda x: extract_features_wrapper(x, extract_features))
    extracted_features_textblob_from_review = df['attributes'].apply(
        lambda x: extract_features_wrapper(x, extract_features_textblob))
    review_features = {"review_data": extracted_features_from_review.tolist()}
    review_features_textblob = {
        "review_data": extracted_features_textblob_from_review.tolist()}
    write_output("extracted_features_spacy.json", review_features)
    write_output("extracted_features_textblob_polarity.json",
                 review_features_textblob)
    aspects = [
        "Value for money",
        "Performance",
        "Scalability",
        "Interoperability",
        "Accessibility",
        "Reliability",
        "Availability",
        "Security",
        "Compliance",
        "Easy setup"
    ]
    absa_tokenizer, absa_model = init_sentiment_model()
    asba_data = df["attributes"].apply(lambda x: get_aspect_analysis_all_aspects_per_field(
        x, aspects, absa_tokenizer, absa_model)).tolist()
    res = {"review_data": asba_data}
    # Writing as txt file due Object32 Serializibility issue
    with open("./outputs/aspect_scores_2.txt", "w") as f:
        f.write(str(res))
