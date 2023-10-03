import pandas as pd

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
        if p != target_projectID:
            similarity = jaccard_similarity(target_tags, t)
            ## codechef: 0.9, codeforces: 0.6
            if similarity > 0.6:
                print(p + " " + str(similarity))
                similar_tags.update(t)
    
    # Find problems associated with similar tags
    recommended_problems = []
    for p, t in projectID_tags_dic.items():
        if p != target_projectID:
            if any(tag in similar_tags for tag in t):
                ## TODO:  add another conditions
                recommended_problems.append(projectID)
    
    return recommended_problems


if __name__ == '__main__':
    # Example usage
    ## Read the problem file
    # df = pd.read_csv('data/codechef/problem.csv')
    df = pd.read_csv('data/codeforces/problem.csv')
    projectID = '1847D'
    recommendations = get_recommendations(df, projectID)
    # print(f"Recommended problems for '{problem}': {recommendations}")