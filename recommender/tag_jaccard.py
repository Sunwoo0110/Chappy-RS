import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
from tqdm import tqdm

## Jaccard similarity
def jaccard_similarity(tag_set1, tag_set2):
    intersection = len(tag_set1.intersection(tag_set2))
    union = len(tag_set1.union(tag_set2))
    return intersection / union

# Create a dictionary to map problems to their tags
def projectID_tags_mapping(df):
    projectID_tags_dic = {}
    for index, row in df.iterrows():
        tags = set(row['tags'].strip("[]").replace("'", "").split(", "))
        projectID_tags_dic[row['projectID']] = tags
        
    return projectID_tags_dic 

# Get recommended problems for a given problem
def get_recommendations(df, target_projectID):
    projectID_tags_dic = projectID_tags_mapping(df)
    target_tags = projectID_tags_dic.get(target_projectID)
    if target_tags is None:
        return []
    
    # Find similar tags
    similar_tags = set()
    for p, t in projectID_tags_dic.items():
        try:
            if p == target_projectID:
                continue
            
            similarity = jaccard_similarity(target_tags, t)
            ## codechef: 0.6, codeforces: 0.6
            if similarity > 0.6:
                print(p + " " + str(similarity))
                # print(t)
                similar_tags.update(t)
        except:
            continue
    print(target_tags)
    print(similar_tags)
    
    # Find problems associated with similar tags
    recommended_problems = []
    for p, t in projectID_tags_dic.items():
        try:
            if p == target_projectID:
                continue
            
            ## similar_tags 중 하나라도 포함되면
            # for tag in t:
            #     if tag in similar_tags:
            #         print(p + " " + tag)
            #         recommended_problems.append(p)
            #         break
            
            ## similar_tags 모두 포함되면
            # if similar_tags.issubset(t):
            #     print(p + " " + str(t))
            #     recommended_problems.append(p)
            
            ## Jaccard similarity
            similarity = jaccard_similarity(t, similar_tags)
            ## codechef: 0.4, codeforces: 0.6
            if similarity > 0.5:
                print(p + " " + str(similarity))
                recommended_problems.append(p)
                
        except:
            continue

    return recommended_problems


if __name__ == '__main__':
    # Example usage
    ## Read the problem file
    # df = pd.read_csv('data/codechef/problem.csv')
    df = pd.read_csv('data/codeforces/problem.csv')
    # projectID = '1847F'
    # recommendations = get_recommendations(df, projectID)
    # print(recommendations)
    
    f = open("data/codeforces/recommendation/jaccard.csv", "w")
    writer = csv.writer(f)
    writer.writerow(['problemID', 'recommendation'])
    
    for projectID in tqdm(df['projectID']):
        recommendations = get_recommendations(df, projectID)
        print(projectID)
        print(recommendations)
        writer.writerow([projectID, recommendations])
        # recommendations_df.append({'projectID': projectID, 'recommendation': recommendations}, ignore_index=True)
    f.close()