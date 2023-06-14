import ssl
import ast
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from distances import calculate_distance
ssl._create_default_https_context = ssl._create_unverified_context


# Function to read the database
def read_data():
    """Read the data from the csv file and return it as a pandas dataframe"""
    data = pd.read_csv('datas/FINAL_DATASET.csv')
    return data

# Function to filter the dataset based on the skills
def filter_skills(row,target_skills):
    skills = ast.literal_eval(row['skills'])
    for skill in skills:
        if skill in target_skills:
            return True
    return False

# Function to retrieve the recommendations
def get_recommendations(job_type, location, enterprise_type, target_skills):

    # Read the data
    dataset = read_data()

    # Filter the dataset based on the job type
    dataset = dataset[dataset.apply(lambda row: filter_skills(row, target_skills), axis=1)]

    # Calculate the similarity between the job description and the user preferences
    vectorizer = TfidfVectorizer()
    job_desc = dataset['company_offeredRole'] + ' ' + dataset['company_type'] 
    user_preferences = job_type + ' ' + enterprise_type
    X = vectorizer.fit_transform(pd.concat([job_desc,pd.Series(user_preferences)]))
    similarity_scores = cosine_similarity(X[:-1], X[-1])

    # Add the similarity score to the dataset
    dataset['similarity_score'] = similarity_scores

    ##TODO 
    # Attribute a weight to the similarity score
    similarity_weight = 0.8
    distance_weight = 0.2

    # Calculate the weighted similarity score
    dataset['weighted_similarity'] = dataset['similarity_score'] * similarity_weight
    
    # Sort the dataframe by weighted similarity and keep the top 60 results
    dataset = dataset.sort_values(by=['weighted_similarity'], ascending=False).head(60)

    # Calculate the distance between the user location and the job location
    dataset['distance_en_km'] = dataset.apply(lambda row: calculate_distance(row["Company_RoleLocation"], location), axis=1)

    # Normalize the distance
    max_distance = dataset['distance_en_km'].max()
    min_distance = dataset['distance_en_km'].min()
    dataset['normalized_distance'] = (dataset['distance_en_km'] - min_distance) / (max_distance - min_distance)

    # Calculate the weighted distance
    dataset['weighted_distance'] = dataset['normalized_distance'] * distance_weight

    # Calculate the weighted similarity & distance score
    dataset['weighted_similarity_distance'] = round(dataset['weighted_similarity'] - dataset['weighted_distance'], 3)

    # Sort the dataframe by weighted similarity and distance
    dataset = dataset.sort_values(by=['weighted_similarity_distance', 'distance_en_km'], ascending=[False, True])

    # Return the top 5 results
    return dataset[['company_offeredRole', 'Company_Name',"Company_RoleLocation","size", 'distance_en_km', 'weighted_similarity_distance',"requested_url"]].reset_index().head(5)
