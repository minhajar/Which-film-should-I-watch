from operator import index
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

#read the csv file containing the movie dataset

df = pd.read_csv("C:/Users/LenovO/Desktop/projectstuff/scraped_Data.csv")
#print (df.head())

# helping functions
def gettitlefromindex(index):
    return df[df.Rank == index]["Title"].values[0]
def getindexfromtitle(title):
    return df[df.Title == title]["Rank"].values[0]




#select main features

features=['Rating','Votes','Genre','Runtime_in_minutes','Metascore']

#create a column in DF which combines all selected features
for feature in features:
    df[feature] = df[feature].fillna('')

    
def combine_features(row): 
    
        return str(row['Rating'])+" "+str(row['Votes'])+" "+row['Genre']+" "+str(row['Runtime_in_minutes'])+" "+str(row['Metascore'])
    

df["combine_features"] = df.apply(combine_features,axis=1)
#print (df["combine_features"].head())


#create count matrix from this new combined column
cv = CountVectorizer()
countMatrix = cv.fit_transform(df["combine_features"])

#compute the cosine similarity based on the count matrix
cos_sim = cosine_similarity(countMatrix)
movie_user_likes="Joker"

#get index of this movie from its title
movie_index = getindexfromtitle(movie_user_likes)
similar_movies = list(enumerate(cos_sim[movie_index]))

#get a list of similar movies in descending order of similarity score
sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1],reverse=True)

                      

#print titles of the first 10 movies
i=0
for movie in sorted_similar_movies:
    print(gettitlefromindex(movie[0]))
    i=i+1
    if i>10:
        break
