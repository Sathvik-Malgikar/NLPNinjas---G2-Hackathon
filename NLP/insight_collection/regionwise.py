import pandas as pd

# Read CSV file into a DataFrame


def extract_country_name(value):
    # Convert string representation of dictionary to a dictionary object
    value_dict = eval(value)
    # Extract the desired value (adjust key name as per your data structure)
    return value_dict.get('country_name', "NA")  # 0 is default value if key doesn't exist

def extract_star_rating(value):
    # Convert string representation of dictionary to a dictionary object
    value_dict = eval(value)
    # Extract the desired value (adjust key name as per your data structure)
    return value_dict.get('star_rating', 0)  # 0 is default value if key doesn't exist


if __name__=="__main__":
    df = pd.read_csv('reviews.csv')
    # Apply the function to extract the rating value
    df['country_name'] = df['attributes'].apply(extract_country_name)
    df['star_rating'] = df['attributes'].apply(extract_star_rating)

    # Group by 'country' column and calculate average of 'star_rating'
    avg_ratings = df.groupby('country_name')['star_rating'].mean()

    # Merge the average ratings with the original DataFrame based on 'country' column
    df = pd.merge(df, avg_ratings, on='country_name', suffixes=('', '_avg'))

    # Rename the new column to 'avg_rating_per_country'
    df.rename(columns={'star_rating_avg': 'avg_rating_per_country'}, inplace=True)

    df.drop(columns=['country_name',"star_rating"], inplace=True)

    # Write the DataFrame back to CSV with the new column
    df.to_csv('output_file.csv', index=False)