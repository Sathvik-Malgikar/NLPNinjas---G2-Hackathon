import google.generativeai as genai

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY="AIzaSyCK3ETVI79O8EIcgAHWwUY1IVRTQchqZw4"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

import json
def write_json_to_file(data, file_path):
    with open("./outputs/"+file_path, 'w') as file:
        json.dump(data, file, indent=4)

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

keywordsdata = read_json_from_file("./outputs/combined_keywords.json")

query1=f'''hese are the keywords extracted from a set of reviews of a particular product. Analyze these and tell me top 10 things the customers are looking for in this class of product.
{keywordsdata}'''


response = model.generate_content(query1)

query2="give a singular python list of these characteristics and nothing more. Top 10."

response = model.generate_content(query2)

#We infer from this and use it for creation of top 10 things customer asks

print(response.text)

import re

# Define the regular expression pattern to match continuous phrases of words
pattern = r'\b\w+(?:\s+\w+)*\b'

# Find all matches of the pattern in the paragraph
customer_expectations = re.findall(pattern, response.text)

print(customer_expectations)


write_json_to_file(customer_expectations , "keyword_inferences.json")
