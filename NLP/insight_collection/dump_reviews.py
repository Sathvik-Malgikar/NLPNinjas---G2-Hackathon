import pandas as pd

df = pd.read_csv("./outputs/reviews.csv")

dump =""
n=0
def dump_reviews(ele):
    global dump,n
    try:
        ele = eval(ele)
        line = f"Title : {ele["title"]} | Question : {ele["comment_answers"]["love"]["text"]} | Answer : {ele["comment_answers"]["love"]["value"]} | Question : {ele["comment_answers"]["hate"]["text"]} | Answer : {ele["comment_answers"]["hate"]["value"]}\n"
        dump+=line
        line=""
    except KeyError as e:
        n+=1
        print(e)
        print("skipped row")

df['attributes'].apply(dump_reviews)

with open("./outputs/review_dump.txt" , "w") as file:
    dump = dump.encode('ascii', 'ignore').decode()
    print(f"skipped {n}lines")
    print(dump , file=file)