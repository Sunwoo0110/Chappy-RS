import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
from tqdm import tqdm

## TF-IDF Cosine Similarity
def tfidf_cosine_similarity(problem1, problem2):
    # Combine the problem descriptions for TF-IDF calculation
    problem_descriptions = [problem1, problem2]
    
    # Initialize TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer()
    
    # Calculate TF-IDF vectors
    tfidf_matrix = tfidf_vectorizer.fit_transform(problem_descriptions)
    
    # Calculate Cosine Similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return similarity[0][0]

## Create a dictionary to map problems to their tags
def projectID_problem_mapping(df):
    projectID_problem_dic = {}
    for index, row in df.iterrows():
        problem = row['problem']
        projectID_problem_dic[row['projectID']] = problem
        
    return projectID_problem_dic 

## Get recommended problems for a given problem
def get_recommendations(df, target_projectID):
    projectID_problem_dic = projectID_problem_mapping(df)
    target_problem = projectID_problem_dic.get(target_projectID)
    if target_problem is None:
        return ""
    
    similarities = []
    recommended_problems = []
    for p, prob in projectID_problem_dic.items():
        try:
            if p == target_projectID:
                continue
            similarity = tfidf_cosine_similarity(target_problem, prob)
            # print(p + " " + str(similarity))
            # similarities.append((p, similarity))
            ## codchef: 0.4, codeforces: 0.7
            if similarity > 0.55:
                print(p + " " + str(similarity))
                recommended_problems.append(p)
        except:
            continue
    
    # # Sort by similarity in descending order
    # similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    
    # # Get recommended problems
    # # codchef: 0.4, codeforces: 0.7
    # recommended_problems = [p for p, s in similarities if s > 0.7]
    
    return recommended_problems

if __name__ == '__main__':
    # Example usage
    ## Read the problem file
    # df = pd.read_csv('data/codechef/problem.csv')
    df = pd.read_csv('data/codeforces/problem.csv')
    # projectID = 'START01'
    # projectID = '1847F'
    # recommendations = get_recommendations(df, projectID)
    # print(recommendations)
    # recommendations_df = pd.DataFrame(columns=['problemID', 'recommendation'])
    
    # f = open("data/codechef/recommendation/TFIDF.csv", "w")
    f = open("data/codeforces/recommendation/TFIDF.csv", "w")
    writer = csv.writer(f)
    writer.writerow(['problemID', 'recommendation'])
    
    for projectID in tqdm(df['projectID']):
        recommendations = get_recommendations(df, projectID)
        print(projectID)
        print(recommendations)
        writer.writerow([projectID, recommendations])
        # recommendations_df.append({'projectID': projectID, 'recommendation': recommendations}, ignore_index=True)
    f.close()

