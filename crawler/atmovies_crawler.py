
# coding: utf-8

# In[1]:


import re
import json
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime


today = time.strftime("%Y%m%d", time.localtime())


total_counter = 0
one_result_counter = 0
perfectly_matched_result_counter = 0
no_movie_data_counter = 0
more_results_counter = 0
no_data_counter = 0

movies_reviews_dict = {}

def movies_crawler(movie_title):    
    
    global total_counter
    total_counter += 1

    search_url = 'http://search.atmovies.com.tw/search/'
    headers = {'Referer':'http://search.atmovies.com.tw/search/'}
    form_data = {'type':'movie','search_term':movie_title}
    r = requests.post(search_url, data = form_data, headers = headers)
    s = BeautifulSoup(r.text, "html5lib")

    movie_value_dict = {}

    if s.select('blockquote > header') != []:
        
        result_type_list = []
        possible_title_ch_list = []
        possible_title_en_list = []
        possible_href_list = []
        
        possible_title_ch_nomoviedata_list = []
        possible_title_en_nomoviedata_list = [] 
        
        for i in range(len(s.select('blockquote > header'))):
            result_type = s.select('blockquote > header')[i].select('font')[0].text
            result_type_list.append(result_type)
            movie_title_xs = movie_title.replace(' ', '')
            
            movie_title_raw = s.select('blockquote > header')[i].select('a')[0].text
            movie_title_ch = movie_title_raw.split(" ")[0]
            if movie_title_ch not in possible_title_ch_nomoviedata_list:
                possible_title_ch_nomoviedata_list.append(movie_title_ch)
            
            movie_title_en = ''.join(movie_title_raw.split(" ")[1:])
            if movie_title_en not in possible_title_en_nomoviedata_list:
                possible_title_en_nomoviedata_list.append(movie_title_en)
                
            if s.select('blockquote > header')[i].select('font')[0].text == '電影' and int(s.select('blockquote > header')[i].select('font')[1].text) < 2018 : 

                movie_review_href = s.select('blockquote > header')[i].select('a')[0]['href']

                if len(s.select('blockquote > header')) == 1:
                    global one_result_counter
                    one_result_counter += 1

                    movie_value_dict['name'] = movie_title_ch
                    movie_value_dict['memo'] = 'only 1 result'
                    movie_value_dict['Ename'] = movie_title_en
                    movie_value_dict['href'] = movie_review_href
                    movies_reviews_dict[movie_title] = movie_value_dict
                    print('movie_title: %s, one_result_counter: %s'%(movie_title, one_result_counter))

                else:

                    if movie_title_xs == movie_title_en:
                        global perfectly_matched_result_counter
                        perfectly_matched_result_counter += 1
                        
                        movie_value_dict['name'] = movie_title_ch
                        movie_value_dict['memo'] = 'perfectly matched result'
                        movie_value_dict['Ename'] = movie_title_en
                        movie_value_dict['href'] = movie_review_href
                        movies_reviews_dict[movie_title] = movie_value_dict
                        print('movie_title: %s, perfectly_matched_result_counter: %s'%(movie_title, perfectly_matched_result_counter))

                        break

                    else:
                        possible_title_en_list.append(movie_title_en)
                        possible_title_ch_list.append(movie_title_ch)
                        possible_href_list.append(movie_review_href)                        
        
        if '電影' not in result_type_list: #或if not...in...
            global no_movie_data_counter
            no_movie_data_counter += 1
            
            movie_value_dict['name'] = possible_title_ch_nomoviedata_list
            movie_value_dict['memo'] = 'no movie data @atmovies'
            movie_value_dict['possible_title_en'] = possible_title_en_nomoviedata_list
            movies_reviews_dict[movie_title] = movie_value_dict
            print('movie_title: %s, no_movie_data_counter: %s'%(movie_title, no_movie_data_counter))
            
        elif movies_reviews_dict == {}: #不穩定
            global more_results_counter
            more_results_counter += 1
            
            movie_value_dict['name'] = possible_title_ch_list
            movie_value_dict['memo'] = 'need more detailed codes'
            movie_value_dict['movie_title_xs'] = movie_title_xs #global movie_title_xs
            movie_value_dict['possible_title_en'] = possible_title_en_list
            movie_value_dict['href'] = possible_href_list ##            
            movies_reviews_dict[movie_title] = movie_value_dict
            print('movie_title: %s, more_results_counter: %s'%(movie_title, more_results_counter))

    else:
        global no_data_counter
        no_data_counter += 1
        
        movie_value_dict['memo'] = 'no data @atmovies'
        movies_reviews_dict[movie_title] = movie_value_dict
        print('movie_title: %s, no_data_counter: %s'%(movie_title, no_data_counter))



    
if __name__ == "__main__":
    

    numThread = 100
    threads = ThreadPoolExecutor(numThread)
    futures = []
    thStart = datetime.now()

    with ThreadPoolExecutor(max_workers=numThread) as executor:
    
        with open('/home/ubuntu/Desktop/movies_title.json') as f:
            movies_title = json.loads(f.read())
            for j in range(len(movies_title)):
                movie_title = movies_title[j]
                futures.append(threads.submit(movies_crawler, movie_title)) #查詢結果不在一起不ok
    
    wait(futures)
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
    print("執行緒:" + str(numThread))    
    print("耗時:" + timeSpent)

    
    
    #記得打開！！！
    with open('movies_title_ch_backup_%s_v2.json'%today, 'w') as f:
        f.write(json.dumps(movies_reviews_dict, ensure_ascii=False, indent=4))
    
    print('\n' + 'REPORT:')
    print('total_counter: %s'%total_counter)
    print('\n')
    print('one_result_counter: %s'%one_result_counter)
    print('perfectly_matched_result_counter: %s'%perfectly_matched_result_counter)
    print('no_movie_data_counter: %s'%no_movie_data_counter)
    print('more_results_counter: %s'%more_results_counter)
    print('no_data_counter: %s'%no_data_counter)
    print('\n' + 'movies_reviews_dict:')
    

