import pandas as pd

# Read CSV file into a DataFrame

upvotes =0
downvotes = 0
totalvotes = 0
def extract_vote_counts(value):
    global upvotes,downvotes,totalvotes
    # Convert string representation of dictionary to a dictionary object
    data = eval(value)
    # Extract the desired value (adjust key name as per your data structure)
    upvotes += data.get('votes_up', 0)  # 0 is default value if key doesn't exist
    downvotes += data.get('votes_down', 0)  # 0 is default value if key doesn't exist
    totalvotes += data.get('votes_total', 0)  # 0 is default value if key doesn't exist

def getvotesinfo():
    return totalvotes,upvotes,downvotes

if __name__ =="__main__":
    df = pd.read_csv('reviews.csv')
    df['attributes'].apply(extract_vote_counts)

    print(f"Total votes are {totalvotes}, upvotes are {upvotes} and downvotes are {downvotes}.")