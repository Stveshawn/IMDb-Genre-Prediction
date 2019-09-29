#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


url_base = 'https://www.imdb.com'


# In[3]:


# A. get all genres and counts
print('1. Start scraping IMDb genres and pages ...', end='\r')
url_genre = 'https://www.imdb.com/search/title/?genres=adventure&genres=Adventure&explore=title_type,genres&ref_=adv_explore_rhs'
response = requests.get(url_genre)
soup = BeautifulSoup(response.text, 'lxml')

Genres = []
g_list = soup.select('.aux-content-widget-2 td')
parse_int = lambda x: int(re.sub('\(|\)|,', '', x)) # helper function to parse int from string
for g in g_list:
    a = g.find('a')
    if a.get('href').find('title_type=') < 0:
        tmp = g.text.split()
        tmp = tmp[0].lower(), parse_int(tmp[1])
        Genres.append(tmp)


# In[6]:


# B. fetch page urls according to each genre
Pages = {}
npage = 2
nn = len(Genres)
for i, (genre, _) in enumerate(Genres):
    for start_page in [i*50+1 for i in range(npage)]:
        url_basesearch = 'https://www.imdb.com/search/title/?genres={}&start={}'.format(genre, str(start_page))
        response = requests.get(url_basesearch)
        soup2 = BeautifulSoup(response.text, 'lxml')
        items = soup2.select('.lister-item-header a')
        for item in items:
            name = item.text
            link = url_base + item.get('href')
            if name in Pages:
                continue
            Pages[name] = link
    print('1. Scraping IMDb genres and pages {:.2f}% ... '.format(i/nn * 100), end='\r')
print('1. Done scraping IMDb genres and pages.                                    ')

# In[8]:


# C. get poster urls from each page
print("2. Start scraping IMDb movie poster urls ...", end='\r')
Posters = []
nn = len(Pages)
for i, (name, link) in enumerate(Pages.items()):
    response = requests.get(link)
    soup3 = BeautifulSoup(response.text, 'lxml')
    gs = list(map(lambda x: x.text, soup3.select('.subtext a')[:3])) # genres
    url_poster = soup3.select('#title-overview-widget img')[0].get('src') # url_poster
    if url_poster.find('nopicture') >= 50:
        continue
    Posters.append((name, link, gs, url_poster))
    print('2. Scraping IMDb movie poster urls  {:.2f}% ... '.format(i/nn * 100), end='\r')
print('2. Done scraping IMDb movie poster urls.                                   ')


# In[10]:


df = pd.DataFrame(Posters, columns=['movie_name', 'url_page', 'genres', 'url_poster'])


# In[75]:


first_g = list(map(lambda x: x[0], df.genres))
c = Counter(first_g) # count number of different genres
c = sorted(c.items(), key=lambda x:x[1])
c = [g for (g, n) in c if n >= 0] # thresholding, delete categories of size < 50
in_sample = list(map(lambda x: x[0] in c, df.genres))


# In[126]:


df['in_sample'] = in_sample
df['main_genre'] = first_g


# In[148]:


# delete minor classes
df2 = df[df.in_sample]
df2 = df2.reset_index(drop=True)
if 'url_poster.csv' not in os.listdir():
    df2.to_csv('url_poster.csv', index=False)
    print('save url_poster.csv to current directory.')


# In[89]:


# make directories to download posters
if 'posters' not in os.listdir():
    os.mkdir('posters')
    print('create directory posters.')


# In[155]:


# D. download posters as png in folder 'posters'
# helper function to download posters
def get_poster(url, fname):
    """download poster from url"""
    f = open('posters/'+fname + '.png', 'wb')
    f.write(requests.get(url).content)
    f.close()
    
print("3. Start downloading IMDb movie posters ...", end='\r')
nn = len(df2)
for i in range(nn):
    tmp = df2.iloc[i]
    get_poster(tmp.url_poster, str(i))
    print('3. Downloading IMDb movie posters {:.2f}% ... '.format(i/nn * 100), end='\r')
print('3. Done downloading IMDb movie posters                           '.format(i/nn * 100))


# In[179]:

