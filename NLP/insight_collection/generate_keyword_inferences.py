import google.generativeai as genai


import json
import pandas as pd

def write_output(filename, data):
    with open("./outputs/"+filename, 'w') as file:
        json.dump(data, file, indent=4)
        
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_keywords(column_value,review_id):
    try:
        
        data = eval(column_value)
        love_keywords = data["love_keywords"]
        hate_keywords = data["hate_keywords"]
        
        return ({"review_id" : review_id, "love_keywords" : love_keywords,"hate_keywords" : hate_keywords})
    except Exception as e:
        print(e)
        print("keyword extraction failed!")

def remove_weights():
    keywordsdata = read_json_from_file("./outputs/combined_keywords.json")
    for key in keywordsdata :
        keywordsdata[key]["love_keywords"] = list(map(lambda a:a[0], keywordsdata[key]["love_keywords"]))
        keywordsdata[key]["hate_keywords"] = list(map(lambda a:a[0], keywordsdata[key]["hate_keywords"]))
    write_output("combined_keywords.json",keywordsdata)
    

def merge_keywords_set():
    keywords_set_1 = read_json_from_file("./outputs/weighted_keywords_yake.json")
    keywords_set_2 = pd.read_csv('./outputs/reviews_bert_keywords.csv')
    
    keywords_set_2 = keywords_set_2.apply(lambda row: read_keywords(row['attributes'], row['id']), axis=1)
    keywords_set_2 = keywords_set_2.reset_index().to_dict(orient='records')
    
    augdata = {}
    for ele in keywords_set_2:
        # print(ele[0])
        augdata[ele[0]["review_id"]] = {"love_keywords": ele[0]["love_keywords"], "hate_keywords": ele[0]["hate_keywords"]}
    
    keywords_set_2 = augdata
    write_output("weighted_keywords_bert.json",keywords_set_2)
    
    combined_set = {}
    # MERGE SETS NOW
    # print ("7098976" in keywords_set_1)
    # print (7098976 in keywords_set_2)
    review_ids =  set.union(set(keywords_set_1.keys()),set(map(str,keywords_set_2.keys()))) 
    for r_id in review_ids:
        temp_l_words=[]
        temp_h_words=[]
        if r_id in keywords_set_1:
            temp_l_words.extend(keywords_set_1[r_id]["love_keywords"])
            temp_h_words.extend(keywords_set_1[r_id]["hate_keywords"])
            
        if int(r_id) in keywords_set_2:
            temp_l_words.extend(keywords_set_2[int(r_id)]["love_keywords"])
            temp_h_words.extend(keywords_set_2[int(r_id)]["hate_keywords"])
        
        combined_set[r_id] = {"love_keywords": temp_l_words, "hate_keywords": temp_h_words}
    
    write_output("combined_keywords.json",combined_set)
    
if __name__ == "__main__":
    # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
    GOOGLE_API_KEY="AIzaSyAZ0zVfwbUmzGls495gZWjutmDcnh26uOw"
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    merge_keywords_set()
    remove_weights()
    
        
    keywordsdata = read_json_from_file("./outputs/combined_keywords.json")

    query1=f'''Following are the keywords extracted from a set of reviews of a particular product. Analyze these and tell me top 10 things the customers are looking for in this class of product. '______' represents the start and end of keywords data
    _______START_______
    {keywordsdata}
    _______END_______
    '''


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


    write_output("keyword_inferences.json" , customer_expectations)
