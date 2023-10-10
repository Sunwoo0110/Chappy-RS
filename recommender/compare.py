import csv
from tqdm import tqdm 

# Convert to set
def parse_recommendations(recommendation):
    return set(recommendation.strip('[]').replace("'", "").split(", "))

# Jaccard CSV file
with open('data/codechef/recommendation/jaccard.csv', 'r') as file1:
    reader = csv.DictReader(file1)
    data1 = list(reader)

# TFIDF CSV file
with open('data/codechef/recommendation/TFIDF.csv', 'r') as file2:
    reader = csv.DictReader(file2)
    data2 = list(reader)

f = open("data/codechef/recommendation/compare.csv", "w")
writer = csv.writer(f)
writer.writerow(['problemID', 'jaccard_count', 'TFIDF_count','percentage', 'same_count', 'different_count'])

for row1, row2 in zip(data1, data2):
    problemID = row1['problemID']
    rec1 = parse_recommendations(row1['recommendation'])
    rec2 = parse_recommendations(row2['recommendation'])
    
    common_elements = rec1.intersection(rec2)
    same_count = len(common_elements)
    different_count = len(rec1) + len(rec2) - 2*same_count
    
    percentage = (same_count / len(rec1)) * 100 if len(rec1) > 0 else 0
    
    writer.writerow([problemID, len(row1['recommendation']), len(row2['recommendation']), percentage, same_count, different_count])
    
f.close()
