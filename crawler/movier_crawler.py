
# coding: utf-8

# In[9]:


import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, wait

import re
import time
from datetime import datetime

import pickle
with open("id_enname_chname_year","rb") as f:
    classifier_list = pickle.load(f)

today = time.strftime("%Y%m%d", time.localtime())

review_counter = 0

def crawler(page):
    DOMAIN_page = 'http://www.movier.tw/bar.php?page={}&STYPE=0&ORDER=date'.format(page)
    r = requests.get(DOMAIN_page)
    r.encoding = 'utf-8'
    s = BeautifulSoup(r.text, "html5lib")
    
    article_num = len(s.select('.td.list-title > span > a'))
    for i in range(article_num):
        
        try:
            movie_title = s.select('.td.list-movie > a')[i].text
        except IndexError:
            movie_title = 'no data'    
        
        print(movie_title)
        

        for movie in classifier_list:
            if movie[3] == movie_title: #or movie[1] in movie_title:
                
                DOMAIN_post= 'http://www.movier.tw/'
                review_url = DOMAIN_post + s.select('.td.list-title > span > a')[i]['href']
                r_url = requests.get(review_url)
                r_url.encoding = 'utf-8'
                s_url = BeautifulSoup(r_url.text, "html5lib")
                
                post_num = len(s_url.select('.post-body > p'))
                parts_list = []
                for i in range(post_num):
                    parts = s_url.select('.post-body > p')[i].text.replace('\xa0', '').replace('⁪&nbsp;','').strip()
                    parts_list.append(parts)
                comment = ''.join(parts_list)
                #print(comment)
                
                raw_dict[movie[0]]['comment'].append(comment)
                
                print('movie: %s'%movie)
                print('movie_title: %s'%movie_title)
        
                global review_counter
                review_counter +=1
                print(review_counter)
                
                del comment
                break

    print("page:" + str(page)+ " done")
        
    
if __name__ == "__main__":
    
    with open("/Users/mac/Desktop/BB104/專題/暫存/format3_.json", "r", encoding="utf-8") as r:
        raw_dict = json.loads(r.read())
    
    last_page = 2 #should be 430
    
    futures = []
    num_thread = 50
    threads = ThreadPoolExecutor(num_thread)
    
    for page in range(1, last_page+1):
        futures.append(threads.submit(crawler, page))
    wait(futures)
    
    for page in range(1, last_page+1):
        futures.append(threads.submit(crawler, page))
    wait(futures)
    
    with open("clean_reviews_movier_test2.json","w", encoding="utf-8") as w:
        w.write(json.dumps(raw_dict, ensure_ascii=False))

