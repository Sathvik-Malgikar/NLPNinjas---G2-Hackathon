import pandas as pd
import json

from regionwise import extract_country_name, extract_star_rating
from getloveandhateinfo import get_love_and_hate_comment_keywords
from vote_counter import extract_vote_counts, getvotesinfo
from average_secondary_metrics import extract_secondary_comments_value, get_avg_values


def write_output(data):
    with open("insights.json", 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    df = pd.read_csv('reviews.csv')
    output = {}

    # votes aggregation

    df['attributes'].apply(extract_vote_counts)
    totalvotes, upvotes, downvotes = getvotesinfo()

    data = {
        "totalvotes": totalvotes,
        "upvotes": upvotes,
        "downvotes": downvotes,

    }
    output["votes_aggregation"] = data

    # regionwise star rating

    # Apply the function to extract the rating value
    df['country_name'] = df['attributes'].apply(extract_country_name)
    df['star_rating'] = df['attributes'].apply(extract_star_rating)

    # Group by 'country' column and calculate average of 'star_rating'
    avg_ratings = df.groupby('country_name')['star_rating'].mean()
    data = avg_ratings.reset_index().to_dict(orient='records')
    output["regionwise_rating"] = data

    # love ane hate keywords
    weighted_keywords = df.apply(lambda row: get_love_and_hate_comment_keywords(
        row['attributes'], row['id']), axis=1)
    data = weighted_keywords.reset_index().to_dict(orient='records')
    output["weighted_keywords"] = data

    # average_secondary_metrics
    df['attributes'].apply(extract_secondary_comments_value)
    data = get_avg_values()
    output["average_secondary_metrics"] = data

    write_output(output)
