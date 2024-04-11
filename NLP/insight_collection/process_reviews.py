import pandas as pd
import json

from regionwise import extract_country_name, extract_star_rating
from getloveandhateinfo import get_love_and_hate_comment_keywords
from vote_counter import extract_vote_counts, getvotesinfo
from average_secondary_metrics import extract_secondary_comments_value, get_avg_values


def write_output(filename, data):
    with open("./outputs/"+filename, 'w') as file:
        json.dump(data, file, indent=4)


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
    write_output("weighted_keywords.json", data)

    # average_secondary_metrics
    df['attributes'].apply(extract_secondary_comments_value)
    data = get_avg_values()

    write_output("average_secondary_metrics.json", data)
