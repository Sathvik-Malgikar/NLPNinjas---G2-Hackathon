import json

def read_json_from_file(file_path):
    with open("./outputs/" +file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

from heapq import heappush,heappop

def get_relevant_reviews(filters , num_reviews =3 ):
    data = read_json_from_file("aspect_scores.json")
    n = len(filters)
    reviews=[]
    ans=[]
    def get_score(obj):
        total=0
        for filt in filters:
            total+=obj[filt]
        return total /n
    for ele in data:
        val = get_score(ele["scores"])
        heappush(reviews , (-val , ele["review_id"]))
    
    for i in range(num_reviews):
        val  =heappop(reviews)
        ans.append(val[1])
    
     
    return ans


if __name__=="__main__":
    print(get_relevant_reviews(["Scalability","Accessibility"]))