import pandas as pd
import requests 
from bs4 import BeautifulSoup
import numpy as np

url = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

rank=[]
title=[]
year=[]
runtime_min=[]
genre=[]
votes=[]
rating=[]
gross=[]
metascore=[]

# extract data of each class in the site and stored in movie_data variable 
movie_data = soup.findAll('div' , attrs={'class' , 'lister-item mode-advanced'})

for store in movie_data:
    movie_rank=store.h3.find('span' , class_="lister-item-index unbold text-primary").text
    rank.append(movie_rank)

    movie_title = store.h3.a.text #without the .text we ll get the whole tag line in html version
    title.append(movie_title)
    
    movie_year = store.h3.find('span', class_="lister-item-year text-muted unbold").text.replace('(','').replace(')','')
    year.append(movie_year)
    
    movie_runtime=store.p.find('span', class_="runtime").text.replace('min', '')
    runtime_min.append(movie_runtime)
    
    
    movie_genre = store.p.find('span', class_="genre").text.replace('\n','').replace(' ','')
    genre.append(movie_genre)
    
    
    ratings_bar=store.find_all('span' , attrs ={'name' : 'nv'})
    vote=ratings_bar[0].text
    votes.append(vote)

    rate = store.find('div', class_="inline-block ratings-imdb-rating").text.replace('\n','')
    rating.append(rate)

    
    earnings = ratings_bar[1].text if len(ratings_bar) > 1 else 'none'
    gross.append(earnings)
    
    movie_metascore = store.find('span' ,class_='metascore').text.replace(' ','') if store.find('span' ,class_='metascore') else 'none'
    metascore.append(movie_metascore)

movie_DF = pd.DataFrame({"Rank" : rank ,"Name_of_movie" : title ,"Year_of_release" : year, "Runtime_in_minutes" : runtime_min, "Genre" : genre, "Votes" : votes , "Rating" : rating , "Metascore" : metascore , "Earnings" : gross})

movie_DF.to_csv("scraped_Data.csv")

#N=np.count_nonzero(title)
#print(N)
print(movie_DF)
