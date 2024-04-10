import pandas as pd
import statistics

# Read CSV file into a DataFrame
df = pd.read_csv('reviews.csv')

ease_of_use = []
meets_requirements = []
quality_of_support = []
ease_of_setup = []
ease_of_admin = []
ease_of_doing_business_with = []

def extract_secondary_comments_value(value):
    # global ease_of_use_sum,meets_requirements_sum,quality_of_support_sum,no_of_secondary_comments
    # Convert string representation of dictionary to a dictionary object
    data = eval(value)
    # Extract the desired value (adjust key name as per your data structure)
    secondary_answers = data.get('secondary_answers',dict())  # 0 is default value if key doesn't exist
    
    
    val = secondary_answers.get('ease_of_use')  # 0 is default value if key doesn't exist
    if val is not None:
        ease_of_use.append(val["value"])
        
    val = secondary_answers.get('meets_requirements')  # 0 is default value if key doesn't exist
    if val is not None:
        meets_requirements.append(val["value"])
        
    val = secondary_answers.get('quality_of_support')  # 0 is default value if key doesn't exist
    if val is not None:
        quality_of_support.append(val["value"])
        
    val = secondary_answers.get('ease_of_setup')  # 0 is default value if key doesn't exist
    if val is not None:
        ease_of_setup.append(val["value"])
        
    val = secondary_answers.get('ease_of_admin')  # 0 is default value if key doesn't exist
    if val is not None:
        ease_of_admin.append(val["value"])
        
    val = secondary_answers.get('ease_of_doing_business_with')  # 0 is default value if key doesn't exist
    if val is not None:
        ease_of_doing_business_with.append(val["value"])
   

df['attributes'].apply(extract_secondary_comments_value)

print(f"average score for ease_of_use is {(statistics.mean(ease_of_use))}")
print(f"average score for meets_requirements is {(statistics.mean(meets_requirements))}")
print(f"average score for quality_of_support is {(statistics.mean(quality_of_support))}")
print(f"average score for ease_of_setup is {(statistics.mean(ease_of_setup))}")
print(f"average score for ease_of_admin is {(statistics.mean(ease_of_admin))}")
print(f"average score for ease_of_doing_business_with is {(statistics.mean(ease_of_doing_business_with))}")


    