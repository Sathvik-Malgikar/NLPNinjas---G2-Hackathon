import tempfile
import pickle
import re
import threading
import time
import nbformat
from flask import Flask, Response, jsonify, request
import json
from flask_cors import CORS
from queue import Queue
import asyncio
import pandas as pd
from NLP.data_collection.review_api import get_response_from_endpoint
from NLP.insight_collection.filter_mechanism import get_relevant_reviews
from NLP.insight_collection.rag import init_sentence_transformer_with_db, get_embedding_function, retrieve_similar_docs, retrieve_similar_docs_page_content, extract_fields_from_review
from NLP.insight_collection.aspect_analysis import get_top_aspect_based_reviews
from langchain_community.vectorstores import Chroma

# Flags
KAGGLE_INSTALLED = True

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()
except OSError:
    print("Disabling custom chatbot as kaggle.json is not present")
    KAGGLE_INSTALLED = False


def read_insights(filename):
    with open("./NLP/insight_collection/outputs/" + filename, 'r') as file:
        data = json.load(file)
    return data


app = Flask(__name__)
CORS(app)
queue = Queue()


def replace_line(file_path, line_number, new_string):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_number < 0 or line_number >= len(lines):
        print("Error: Line number out of range")
        return

    lines[line_number] = new_string + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)


def execute_kaggle_notebook(queue):
    kaggle_api.kernels_push_cli("./NLP/insight_collection/kaggle_notebooks")
    while True:
        status = kaggle_api.kernel_status("hemabhushan", "rag-gemma-2")
        if status['status'] == 'complete':
            break
        time.sleep(10)
    queue.put(status['status'])
    return status['status']


def get_rag_gemma_results(file):
    # with open("rag-gemma-2.log", "r", encoding="utf-8") as f:
    #     file = f.read()
    file = str(file['log'])
    results = re.findall(r'StartResults(.*?)EndResults', file, re.DOTALL)
    return results[0]


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/aggregates/average-secondary-metrics')
def get_average_secondary_metrics():
    resp = Response()
    json_data = read_insights("average_secondary_metrics.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


@app.route('/aggregates/votes-data')
def get_votes_data():
    resp = Response()
    json_data = read_insights("votes_aggregation.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


@app.route('/keyword-inferences')
def get_keyword_inferences():
    resp = Response()
    json_data = read_insights("keyword_inferences.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


@app.route('/aggregates/regionwise-rating')
def get_regionwise_rating():
    resp = Response()
    json_data = read_insights("regionwise_rating.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


@app.route('/aggregates/aspect-keywords')
def get_aspect_keywords():
    resp = Response()
    json_data = read_insights("/extracted_features_spacy.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


@app.route('/aggregates/polarity-keywords')
def get_polarity_keywords():
    resp = Response()
    json_data = read_insights("/extracted_features_textblob_polarity.json")
    resp.headers["Content-Type"] = "application/json"
    resp.data = json.dumps(json_data)
    return resp


@app.route("/search/similar-docs", methods=["POST"])
def get_similar_docs():
    resp = Response()
    request_data = request.get_json()
    query = request_data["query"]
    resp.headers["Content-Type"] = "application/json"
    similar_docs = retrieve_similar_docs(query, chroma_db)
    similar_docs_page_content = retrieve_similar_docs_page_content(
        similar_docs)
    json_data = {"data": similar_docs_page_content}
    resp.data = json.dumps(json_data)
    return resp


@app.route('/rag/query', methods=["POST"])
def query_rag_gemma():

    if not KAGGLE_INSTALLED:
        return jsonify({'message': 'Kaggle not installed on backend machine'}), 500

    resp = Response()
    request_data = request.get_json()
    query = request_data["query"]
    new_content = f"""query='{query}'"""
    replace_line(
        "./NLP/insight_collection/kaggle_notebooks/rag_gemma.py", 351, new_content)
    thread = threading.Thread(target=execute_kaggle_notebook, args=(queue,))
    thread.start()
    return jsonify({'message': 'Data processing started'}), 202
    # Wait for notebook execution to complete
    # thread.join()
    # Save the modified notebook
    # results = queue.get()


@app.route('/rag/get-results')
def get_rag_prompt_results():

    if not KAGGLE_INSTALLED:
        return jsonify({'message': 'Kaggle not installed on backend machine'}), 500

    if (queue.qsize() == 0):
        return jsonify({"message": "No results Available"})
    resp = Response()
    results = queue.get()
    resp.headers["Content-Type"] = "application/json"
    if results == 'complete':
        logs = kaggle_api.kernel_output("hemabhushan", "rag-gemma-2")
        res = get_rag_gemma_results(logs)
        data = {"results": res}
        resp.data = json.dumps(data)
    elif results == 'running':
        data = {"results": "Still running"}
        resp.data = json.dumps(data)
    elif results == 'error':
        data = {"results": "Failed to execute prompt on Cloud GPU"}
        resp.data = json.dumps(data)
    return resp


@app.route('/filter-reviews', methods=["GET"])
def get_aspect_filtered_reviews():
    aspects = [request.args.get(f'f{i+1}') for i in range(10)]

    with open("./NLP/insight_collection/outputs/aspect_scores_2.json", "r") as f:
        aspect_file = json.loads(f.read())

    filtered_reviews = get_top_aspect_based_reviews(
        aspect_file["review_data"], aspects)
    reviews = pd.read_csv("./NLP/insight_collection/outputs/reviews.csv")
    filtered_reviews_new = reviews["attributes"].apply(
        extract_fields_from_review).tolist()
    ids = []
    for key, value in filtered_reviews.items():
        ids.extend([x["id"] for x in value])
    # print(type(filtered_reviews_new[0]))
    filtered_reviews_new = list(
        filter(lambda x: x["id"] in ids, filtered_reviews_new))
    resp = Response()
    resp.data = json.dumps(filtered_reviews_new)
    return resp


@app.route('/review-by-id', methods=["GET"])
def get_review_by_id():
    rev_id = request.args.get("id")

    if not rev_id:
        return 'Error: Missing query parameters', 400
    return get_response_from_endpoint("https://data.g2.com/api/v1/survey-responses/" + rev_id)


@app.route('/filter-reviews-2', methods=['GET'])
def get_data():
    # Read query parameters
    f1 = request.args.get('f1')
    f2 = request.args.get('f2')
    f3 = request.args.get('f3')
    f4 = request.args.get('f4')
    f5 = request.args.get('f5')
    f6 = request.args.get('f6')
    f7 = request.args.get('f7')
    f8 = request.args.get('f8')
    f9 = request.args.get('f9')
    f10 = request.args.get('f10')
    num_reviews = request.args.get('num_reviews')

    filtermask = list(map(bool, [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]))
    if not any(filtermask) or not num_reviews:
        return 'Error: Missing query parameters', 400

    rev_ids = get_relevant_reviews(filtermask)

    return rev_ids, 200


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    # chroma_db = init_sentence_transformer_with_db()

    # Persist collection to temporary directory
    # chroma_db.persist()

    # Later, to load the collection from disk
    chroma_db = Chroma(persist_directory="./NLP/insight_collection/outputs/chroma_db",
                       embedding_function=get_embedding_function())
    # documents = chroma_db.get_all()

    # for document in documents:
    #     # Serialize each document with pickle
    #     with open(f"./chroma_db/document_{document['id']}.pkl", "wb") as f:
    #         pickle.dump(document, f)
    app.run()
