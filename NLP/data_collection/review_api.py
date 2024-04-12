
import requests
import json

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_response_from_endpoint(url, headers=None):
    if headers ==None:
        headers = {
    "Authorization": f"Token token={API_KEY}",
    "Content Type": "application/vnd.api+json"
}

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

# Example usage:
# has to be a GET request

import os

API_KEY = os.environ.get("GOOGLE_API_KEY")

custom_headers = {
    "Authorization": f"Token token={API_KEY}",
    "Content Type": "application/vnd.api+json"
}

def process_one_batch(response):
    
    results = read_json_from_file("results.json")

    data = response["data"]
    n=results["num_reviews"]
    sm= results["average_star_rating"]*results["num_reviews"]
    
    for review in data:
        n+=1
        sm+=review["attributes"]["star_rating"]
        
    results["average_star_rating"] =  (sm)/n
    results["num_reviews"]=n
        
        
    write_json_to_file(results,"results.json")

if __name__ =="__main__":
    import time

    url = "https://data.g2.com/api/v1/survey-responses?page%5Bnumber%5D=1&page%5Bsize%5D=10" # param id can be added optionally

    empty_results = {
        "average_star_rating": 0,
        "num_reviews": 0
    }

    write_json_to_file(empty_results,"results.json")

    while True:
        t1 = time.time()
        response = get_response_from_endpoint(url, headers=custom_headers)
        if response:
            write_json_to_file(response,"response.json")
            process_one_batch(response)
            t2 = time.time()
            print(f"Processed one batch in {t2-t1} seconds")
            if "next" in response["links"]:
                
                url = response["links"]["next"]
            else:
                break
            
        else:
            print("Failed to get response from the endpoint.")
            
    print("Processing reviews completed, reached end of linked list")

