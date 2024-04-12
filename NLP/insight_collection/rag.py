from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import pandas as pd


def extract_fields(data):
    data = eval(data)
    product_name = data.get('product_name', '')
    star_rating = data.get('star_rating', '')
    title = data.get('title', '')
    user_name = data.get('user_name', '')
    submitted_at = data.get('submitted_at', '')
    review_source = data.get('review_source', '')
    votes_up = data.get('votes_up', '')
    votes_down = data.get('votes_down', '')
    country_name = data.get('country_name', '')

    love = data['comment_answers'].get('love', {}).get('value', '')
    hate = data['comment_answers'].get('hate', {}).get('value', '')
    benefits = data['comment_answers'].get('benefits', {}).get('value', '')
    recommendations = data['comment_answers'].get(
        'recommendations', {}).get('value', '')

    meets_requirements = data['secondary_answers'].get(
        'meets_requirements', {}).get('value', '')
    ease_of_use = data['secondary_answers'].get(
        'ease_of_use', {}).get('value', '')
    quality_of_support = data['secondary_answers'].get(
        'quality_of_support', {}).get('value', '')
    ease_of_setup = data['secondary_answers'].get(
        'ease_of_setup', {}).get('value', '')
    ease_of_admin = data['secondary_answers'].get(
        'ease_of_admin', {}).get('value', '')
    ease_of_doing_business_with = data['secondary_answers'].get(
        'ease_of_doing_business_with', {}).get('value', '')

    # Construct the string within tags
    result_string = f"""
Product Name: {product_name}
Star Rating: {star_rating}
Title: {title}
User Name: {user_name}
Submitted At: {submitted_at}
Review Source: {review_source}
Votes Up: {votes_up}
Votes Down: {votes_down}
Country Name: {country_name}

Love: {love}
Hate: {hate}
Benefits: {benefits}
Recommendations: {recommendations}

Secondary Answers:
Meets Requirements: {meets_requirements}
Ease of Use: {ease_of_use}
Quality of Support: {quality_of_support}
Ease of Setup: {ease_of_setup}
Ease of Admin: {ease_of_admin}
Ease of Doing Business With: {ease_of_doing_business_with}
"""

    return result_string.strip()


def extract_review_info(review):
    # Extracting attributes
    review = eval(review)
    print(review)
    attributes = review.get("attributes", {})
    product_name = attributes.get("product_name", "")
    star_rating = attributes.get("star_rating", "")
    title = attributes.get("title", "")
    user_name = attributes.get("user_name", "")
    submitted_at = attributes.get("submitted_at", "")
    review_source = attributes.get("review_source", "")
    votes_up = attributes.get("votes_up", "")
    votes_down = attributes.get("votes_down", "")
    country_name = attributes.get("country_name", "")

    # Extracting comment answers
    comment_answers = attributes.get("comment_answers", {})
    love = comment_answers.get("love", {}).get("value", "")
    hate = comment_answers.get("hate", {}).get("value", "")
    benefits = comment_answers.get("benefits", {}).get("value", "")
    recommendations = comment_answers.get(
        "recommendations", {}).get("value", "")

    # Extracting secondary answers
    secondary_answers = attributes.get("secondary_answers", {})
    meets_requirements = secondary_answers.get(
        "meets_requirements", {}).get("value", "")
    ease_of_use = secondary_answers.get("ease_of_use", {}).get("value", "")
    quality_of_support = secondary_answers.get(
        "quality_of_support", {}).get("value", "")
    ease_of_setup = secondary_answers.get("ease_of_setup", {}).get("value", "")
    ease_of_admin = secondary_answers.get("ease_of_admin", {}).get("value", "")
    ease_of_doing_business_with = secondary_answers.get(
        "ease_of_doing_business_with", {}).get("value", "")

    # Constructing content
    content = f"""
    Product Name: {product_name}
    Star Rating: {star_rating}
    Title: {title}
    User Name: {user_name}
    Submitted At: {submitted_at}
    Review Source: {review_source}
    Votes Up: {votes_up}
    Votes Down: {votes_down}
    Country Name: {country_name}
    
    Love: {love}
    Hate: {hate}
    Benefits: {benefits}
    Recommendations: {recommendations}
    
    Secondary Answers:
    Meets Requirements: {meets_requirements}
    Ease of Use: {ease_of_use}
    Quality of Support: {quality_of_support}
    Ease of Setup: {ease_of_setup}
    Ease of Admin: {ease_of_admin}
    Ease of Doing Business With: {ease_of_doing_business_with}
    """

    # Extracting relationships metadata
    relationships = review.get("relationships", {})
    product_link = relationships.get(
        "product", {}).get("links", {}).get("self", "")
    questions_link = relationships.get(
        "questions", {}).get("links", {}).get("self", "")
    answers_link = relationships.get(
        "answers", {}).get("links", {}).get("self", "")

    # Constructing metadata
    metadata = {
        "product_link": product_link,
        "questions_link": questions_link,
        "answers_link": answers_link
    }
    return content.strip()


def extract_review_metadata(review):
    # Extracting attributes
    review = eval(review)

    # Extracting relationships metadata
    relationships = review.get("relationships", {})
    product_link = relationships.get(
        "product", {}).get("links", {}).get("self", "")
    questions_link = relationships.get(
        "questions", {}).get("links", {}).get("self", "")
    answers_link = relationships.get(
        "answers", {}).get("links", {}).get("self", "")

    # Constructing metadata
    metadata = {
        "product_link": product_link,
        "questions_link": questions_link,
        "answers_link": answers_link
    }

    return metadata


def init_sentence_transformer_with_db():
    df = pd.read_csv('./outputs/reviews.csv')
    embedding_function = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2")

    # loader = JSONLoader(file_path="../response.json",
    #                     jq_schema=".data[]", text_content=False)
    # documents = loader.load()
    content = df["attributes"].apply(extract_fields).tolist()
    metadata = df["attributes"].apply(extract_review_metadata).tolist()
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    documents = text_splitter.create_documents(
        content, metadatas=metadata)
    db = Chroma.from_documents(documents, embedding_function)
    return db
    # print(docs[0].page_content)


def retrieve_similar_docs(query, db):
    docs = db.similarity_search(query)
    return docs


def retrieve_similar_docs_page_content(docs):
    return [x.page_content for x in docs]


# print(get_similar_docs("is G2 useful?", init_sentence_transformer_with_db()))
