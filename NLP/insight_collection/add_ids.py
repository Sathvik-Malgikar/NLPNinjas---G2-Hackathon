import pandas as pd
import json


def extract_id(review):
    review = eval(review)
    return review["slug"].split("-")[-1]


if __name__ == "__main__":
    df = pd.read_csv('./outputs/reviews.csv')
    extracted_ids = df["attributes"].apply(extract_id).tolist()
    with open("./outputs/extracted_features_spacy.json", "r") as f:
        file_spacy = json.loads(f.read())
    with open("./outputs/extracted_features_textblob_polarity.json", "r") as f:
        file_textblob = json.loads(f.read())
    for i in range(len(extracted_ids)):
        file_spacy["review_data"][i]["id"] = extracted_ids[i]
        file_textblob["review_data"][i]["id"] = extracted_ids[i]
    with open("./outputs/extracted_features_spacy.json", "w") as f:
        f.write(json.dumps(file_spacy))
    with open("./outputs/extracted_features_textblob_polarity.json", "w") as f:
        f.write(json.dumps(file_textblob))
