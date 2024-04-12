from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline


def init_sentiment_model():
    # Load Aspect-Based Sentiment Analysis model
    absa_tokenizer = AutoTokenizer.from_pretrained(
        "yangheng/deberta-v3-base-absa-v1.1")
    absa_model = AutoModelForSequenceClassification \
        .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
    return absa_tokenizer, absa_model

# Load a traditional Sentiment Analysis model
# sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
# sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
#                           tokenizer=sentiment_model_path)


def get_aspect_analysis_sentence(sentence, aspect, tokenizer, model):
    inputs = tokenizer(
        f"[CLS] {sentence} [SEP] {aspect} [SEP]", return_tensors="pt")
    outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    probs = probs.detach().numpy()[0]
    # print(f"Sentiment of aspect '{aspect}' is:")
    res = {}
    for prob, label in zip(probs, ["negative", "neutral", "positive"]):
        # print(f"Label {label}: {prob}")
        res[label] = prob

    return res


def extract_fields_from_review(json_str):
    data = eval(json_str)
    fields_dict = {
        'id': data.get('slug', '').split("-")[-1],
        'product_name': data.get('product_name', ''),
        'title': data.get('title', ''),
        'love_text': data.get('comment_answers', {}).get('love', {}).get('value', ''),
        'hate_text': data.get('comment_answers', {}).get('hate', {}).get('value', ''),
        'recommendations_text': data.get('comment_answers', {}).get('recommendations', {}).get('value', ''),
        'benefits_text': data.get('comment_answers', {}).get('benefits', {}).get('value', '')
    }

    return fields_dict


def get_aspect_analysis_all_aspects_per_field(review, aspects, tokenizer, model):
    res = {}
    # review=eval(review)
    review_fields = extract_fields_from_review(review)
    res["id"] = review_fields["id"]
    res["product_name"] = review_fields["product_name"]

    for review_field in review_fields.keys():
        if review_field in ["id", "product_name"]:
            continue
        res[review_field] = {}
        for aspect in aspects:
            res[review_field][aspect] = get_aspect_analysis_sentence(
                review_fields[review_field], aspect, tokenizer, model)
    return res


def get_top_aspect_based_reviews(json_list, aspects):
    top_reviews = {aspect: [] for aspect in aspects}
    max_positive_scores = {aspect: -1 for aspect in aspects}

    for review in json_list:
        for aspect in aspects:
            for field in ['title', 'love_text', 'hate_text', 'recommendations_text', 'benefits_text']:
                if aspect in review[field]:
                    positive_score = review[field][aspect]["positive"]
                    if positive_score > max_positive_scores[aspect]:
                        max_positive_scores[aspect] = positive_score
                        top_reviews[aspect].insert(0, review)
                    elif positive_score == max_positive_scores[aspect]:
                        top_reviews[aspect].append(review)

    return top_reviews
