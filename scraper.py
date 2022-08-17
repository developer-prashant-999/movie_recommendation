from re import X
import requests # web page request
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import tqdm

'''
    Works for imdb pages recomend using all the pages with genres information
    discards all the ones with less then 3 genres type. 
'''

def get_all_titles(soup):
    result_topics = []
    all_topics = soup.find_all('h3',{"class":"lister-item-header"})# h3 bhitra xa title
    # print(all_topics)
    for topic in all_topics:
        #logic:
        #<a> Movie name </a>
        #=a= Movie name =/a=
        topic = str(topic.find('a'))
        topic = topic.replace('<',"=")
        topic = topic.replace(">","=")
        topic = topic.split('=')
        topic = topic[int(len(topic)/2)]
        result_topics.append(topic)
    # print(result_topics)
    return result_topics

def get_all_genres(soup):
    result_genres = []
    all_genres = soup.find_all("p",{"class":'text-muted'})# here find_all genres related sab movie ko li dinxa no loop needed
    # print(all_genres)
    for genre in all_genres:
        genre = str(genre.find_all("span",{"class":"genre"}))
        if genre == '[]':
            pass
        else:
            genre = genre.replace('<',"=")
            genre = genre.replace(">","=")
            genre = genre.split('=')
            genre = genre[int(len(genre)/2)]
            result_genres.append(genre)
    # print(result_genres)
    return result_genres

def post_process(genres):
    post_process_genres = []
    for i in genres:
        i = i.replace("\n","")
        i = i.replace(" ","")
        post_process_genres.append(i)
    # print(post_process_genres)
    return post_process_genres

def check_repeated_comma(x):
    list_x = x.split(',')
    if len(list_x)==3:
        return x
    else:
        return np.NaN


def data_set(url):
    data_set = pd.DataFrame(columns = ["Movie","Primary Genre","Secondary Genre","Tertiary Genre"])
    #Initially get the page from the url and from the content extract all the things properly so page is extracted
    page = requests.get(url) # gets entire webpage

    #Soup is created where all the contentis parsed as html format so it can be extracted as seen in webpages.
    soup = BeautifulSoup(page.content, 'html.parser') # gets entire source code for webpage
    #print(soup)

    title = get_all_titles(soup)
    genres = get_all_genres(soup)
    genres = post_process(genres)
    data_set["Movie"]=pd.Series(title)  
    data_set["Primary Genre"]=pd.Series(genres)
    data_set["Primary Genre"]=data_set["Primary Genre"].apply(check_repeated_comma)
    data_set["Secondary Genre"]=data_set["Secondary Genre"].fillna("To Be Filled")
    data_set["Tertiary Genre"]=data_set["Tertiary Genre"].fillna("To Be Filled")
    # print(data_set.head())
    data_set = data_set.loc[data_set["Primary Genre"]!=np.NaN]
    # print(data_set.head())
    data_set = data_set.dropna(how="any")
    data_set[["Primary Genre","Secondary Genre","Tertiary Genre"]] = data_set["Primary Genre"].str.split(',', expand=True)
    data_set.to_csv("Dataset.csv", mode='a', header=False)
    print(data_set.head())

if __name__ == "__main__":
    import os 
    os.system('cls') # run vai ry ko terminal lai clear screen gareko 
    print("IMDB Scrapper")
    # number_of_pages = int(input('Enter the number of various pages to scrap: '))
    # for i in range(number_of_pages):
    #     url = input("Enter the url: ")
    #     data_set(url)
    number_of_genre = int(input("Enter numbers of genre you would like to scrape(<6): "))
    number_of_pages = int(input('Enter the pages for that genre to scrap(<6): '))

    genre_list = ['action', 'adventure', 'comedy', 'horror', 'thriller', 'drama']

    for i in tqdm.tqdm(range(number_of_genre)):
        count = 1
        for j in range(number_of_pages):
            url = f'https://www.imdb.com/search/title/?title_type=feature&genres={genre_list[i]}&start={count}&ref_=adv_nxt'
            count = count + 50
            print(url)
            data_set(url)
