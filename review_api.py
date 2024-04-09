
import requests
import json

def write_json_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

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

# Example usage:
# has to be a GET request
url = "https://data.g2.com/api/v1/survey-responses" # param id can be added optionally

API_KEY = "1da6d9512ad00fc394bd04234bc7358dc9b85d96fa0c56281f710dc9abcef7e5"

custom_headers = {
    "Authorization": f"Token token={API_KEY}",
    "Content Type": "application/vnd.api+json"
}


response = get_response_from_endpoint(url, headers=custom_headers)
if response:
    write_json_to_file(response,"response.json")
else:
    print("Failed to get response from the endpoint.")

