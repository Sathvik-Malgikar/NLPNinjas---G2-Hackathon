import google.generativeai as genai

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY="AIzaSyAZ0zVfwbUmzGls495gZWjutmDcnh26uOw"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

import json

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

keywordsdata = read_json_from_file("./outputs/weighted_keywords.json")

query1=f'''
{keywordsdata}

these are the keywords extracted from a set of reviews of a particular product. Analyze these and tell me top 10 things the customers are looking for in this class of product.'''



response = model.generate_content(query1)

query2="give a singular python list of these characteristics and nothing more. Top 10."

response = model.generate_content(query2)

#We infer from this and use it for creation of top 10 things customer asks
print(response.text)
