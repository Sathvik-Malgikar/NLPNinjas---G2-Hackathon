#!/usr/bin/env python
# coding: utf-8

# # RAG: Using Gemma LLM locally for question answering on private data

# In this notebook, our aim is to develop a RAG system utilizing [Google's Gemma](https://ai.google.dev/gemma) model. We'll generate vectors with [Elastic's ELSER](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html) model and store them in Elasticsearch. Additionally, we'll explore semantic retrieval techniques and present the top search results as a context window to the Gemma model. Furthermore, we'll utilize the [Hugging Face transformer](https://huggingface.co/google/gemma-2b-it) library to load Gemma on a local environment.

# ## Setup

# **Elastic Credentials** - Create an [Elastic Cloud deployment](https://www.elastic.co/search-labs/tutorials/install-elasticsearch/elastic-cloud) to get all Elastic credentials (`ELASTIC_CLOUD_ID`,` ELASTIC_API_KEY`).
#
# **Hugging Face Token** - To get started with the [Gemma](https://huggingface.co/google/gemma-2b-it) model, it is necessary to agree to the terms on Hugging Face and generate the [access token](https://huggingface.co/docs/hub/en/security-tokens) with `write` role.
#
# **Gemma Model** - We're going to use [gemma-2b-it](https://huggingface.co/google/gemma-2b-it), though Google has released 4 open models. You can use any of them i.e. [gemma-2b](https://huggingface.co/google/gemma-2b), [gemma-7b](https://huggingface.co/google/gemma-7b), [gemma-7b-it](https://huggingface.co/google/gemma-7b-it)

# ## Install packages

# In[1]:


# pip install -q -U elasticsearch langchain transformers huggingface_hub ray


import json
from huggingface_hub import notebook_login, login
from torch.nn.parallel import DataParallel
from transformers import AutoTokenizer, pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain import HuggingFacePipeline
from langchain.vectorstores import ElasticsearchStore
from langchain.text_splitter import CharacterTextSplitter
from elasticsearch import Elasticsearch, helpers
import gc
import ray
import torch
import requests
from urllib.request import urlopen
from getpass import getpass
import os
import subprocess

# Define the pip command
pip_command = ['pip', 'install', '-q', '-U', 'elasticsearch',
               'langchain', 'transformers', 'huggingface_hub', 'ray']

# Run the pip command
process = subprocess.Popen(
    pip_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the process to finish
stdout, stderr = process.communicate()

# Check if the installation was successful
if process.returncode == 0:
    print("Packages installed successfully.")
else:
    print("Error installing packages.")
    print("STDOUT:")
    print(stdout.decode())
    print("STDERR:")
    print(stderr.decode())
# ## Import packages

# In[27]:


# ## Get Credentials

# In[9]:


# ELASTIC_API_KEY = getpass("Elastic API Key :")
ELASTIC_API_KEY = "QmhaYXg0NEJTbzNMaVQ0eUVDY3U6V1QzMkZtcWVST3k5VlRCbWlqRFpQQQ=="

# ELASTIC_CLOUD_ID = getpass("Elastic Cloud ID :")
ELASTIC_CLOUD_ID = "RAG_G2:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGNiYWE5N2ZlMWQyYTQ3MTdhYjEzYTNlMmRkM2MyZmExJGVjMWM4MWI2NWRiNjQ5YjRiNDlkOTEyOTdiYzU3YTk2"

elastic_index_name = "gemma-rag"


# ## Add documents

# ### Let's download the sample dataset and deserialize the document.

# In[10]:


# url = "https://raw.githubusercontent.com/elastic/elasticsearch-labs/main/datasets/workplace-documents.json"

# response = urlopen(url)

# workplace_docs = json.loads(response.read())


# In[11]:


def get_response_from_endpoint(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            return None  # Return None if request was not successful
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


# In[12]:


API_KEY = "1da6d9512ad00fc394bd04234bc7358dc9b85d96fa0c56281f710dc9abcef7e5"

custom_headers = {
    "Authorization": f"Token token={API_KEY}",
    "Content Type": "application/vnd.api+json"
}


# In[13]:


def extract_review_info(review):
    # Extracting attributes
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

    return content.strip(), metadata


# ### Split Documents into Passages

# In[14]:


metadata = []
content = []

"""for doc in workplace_docs:
    content.append(doc["content"])
    metadata.append(
        {
            "name": doc["name"],
            "summary": doc["summary"],
            "rolePermissions": doc["rolePermissions"],
        }
    )"""
for i in range(77):
    url = f"https://data.g2.com/api/v1/survey-responses?page%5Bnumber%5D={i+1}&page%5Bsize%5D=10"
    response_data = get_response_from_endpoint(url, custom_headers)
    temp_list = [extract_review_info(review)
                 for review in response_data["data"]]
    content.extend([review_content for review_content, _ in temp_list])
    metadata.extend([review_metadata for _, review_metadata in temp_list])


# In[15]:


text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=0)
docs = text_splitter.create_documents(content, metadatas=metadata)


# ## Index Documents into Elasticsearch using ELSER
#
# Before we begin indexing, ensure you have [downloaded and deployed the ELSER model](https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-elser.html#download-deploy-elser) in your deployment and is running on the ML node.

# In[16]:


es = ElasticsearchStore.from_documents(
    docs,
    es_cloud_id=ELASTIC_CLOUD_ID,
    es_api_key=ELASTIC_API_KEY,
    index_name=elastic_index_name,
    strategy=ElasticsearchStore.SparseVectorRetrievalStrategy(
        model_id=".elser_model_2"
    ),
    request_timeout=180, timeout=180
)

es


# ## Hugging Face login

# In[17]:


os.environ["HUGGINGFACE_TOKEN"] = "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"
login(token="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")

# notebook_login()#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


# ## Initialize the tokenizer with the model (`google/gemma-2b-it`)

# In[18]:


model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2b-it", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")


# In[19]:


# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = model.to(device)


# In[20]:


# model = DataParallel(model)


# ## Create a `text-generation` pipeline and initialize with LLM

# In[21]:


pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=1024,
)

llm = HuggingFacePipeline(
    pipeline=pipe,
    model_kwargs={"temperature": 0.7},
)


# ## Format Docs

# In[22]:


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# ## Create a chain using Prompt template

# In[23]:


retriever = es.as_retriever(search_kwargs={"k": 5})

template = """Answer the question based only on the following context:\n

{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


# ## Ask question

# In[30]:

query = 'hello'
query_res = chain.invoke(query).replace('\n', '')
print(f"StartResults {query_res} EndResults")


# In[28]:


device_ids = [0]  # Assuming you want to clear memory of GPU 0 and GPU 1
devices = [torch.device(f"cuda:{gpu_id}") for gpu_id in device_ids]

# Clear memory for each GPU
for device in devices:
    with torch.cuda.device(device):
        gc.collect()
        torch.cuda.empty_cache()

print("Memory cleared for GPUs:", device_ids)


# In[29]:


# In[31]:


# ray.init()


# In[32]:


"""@ray.remote(num_gpus=2)
class RemoteRetriever:
    def __init__(self):
        self.retriever = retriever

    def retrieve(self, input_query):
        return self.retriever(input_query)

@ray.remote(num_gpus=2)
class RemoteLLM:
    def __init__(self):
        self.llm = llm

    def generate_text(self, input_text):
        return self.llm(input_text)

# Define the pipeline
chain = (
    {"context": RemoteRetriever.remote() | format_docs, "question": RunnablePassthrough()}
    | prompt
    | RemoteLLM.remote()
    | StrOutputParser()
)

# Example usage of the pipeline
input_query = "EXplain about g2"
output = ray.get(chain.run(input_query))
print(output)

# Shutdown Ray
ray.shutdown()"""


# In[ ]:
