
# coding: utf-8

# In[126]:


import csv
import pandas as pd

import time
import random
import requests 
from bs4 import BeautifulSoup as bs
import concurrent.futures

from concurrent.futures import ThreadPoolExecutor, wait

import json
with open("id_list.json", "r", encoding="utf-8") as r:
    id_list = json.loads(r.read())

WORKERNUM = 30
RETRYTIME = 0.3

movie_list = []
watch_dict = {}
user_list = []

dprint = print
def dprint(s):
    True

tStart = time.time()

# get free proxy list
def get_proxy():
    resp = requests.get("https://free-proxy-list.net/")
    iplist = bs(resp.text, "lxml").select_one(".table-striped").select("tbody tr")
    plist = [iplist[i].select("td")[0].text + ":" + iplist[i].select("td")[1].text
            for i in range(len(iplist))]
    return plist

# random choice proxy for crawling
pflag=0
def get_url_data(url):
    global pflag
    global proxies
    if (pflag == 0):
        proxies = get_proxy()
        pflag = 1000
    while True:
        pflag-= 1
        proxy = {'http':'http://' + random.choice(proxies)}
        dprint(proxy)
        try:
            return requests.get(url, proxies=proxy, timeout=(1,3))
        except:
            time.sleep(RETRYTIME)

##
def worker(imdb_id):
    review_url = 'http://www.imdb.com/title/{}/reviews'.format(imdb_id)
    
    resp = get_url_data(review_url)
    while (resp.status_code != 200):
        dprint("retry ...")
        resp = get_url_data(review_url)
        
    soup = bs(resp.text, 'html5lib') #soup = bs(requests.get(review_url).text,"lxml")
    try:
        en_title = soup.select('.parent > h3 > a')[0].text
        review_num = soup.select('.lister > .header > span')[0].text
        movie_list.append([imdb_id, en_title, review_num])
        
        page_user_num = len(soup.select('.display-name-link'))
        for i in range(page_user_num):
            user_account = soup.select('.display-name-link > a')[i].text
            if not user_account in watch_dict:
                watch_dict[user_account] = set([en_title])
                user_list.append(user_account)
            else:
                watch_dict[user_account].update([en_title])
                
        while True:
            try:
                load_data = soup.select('.load-more-data')[0]['data-key']
                load_domain = 'http://www.imdb.com/title/{}/reviews/_ajax?ref_=undefined&paginationKey='.format(imdb_id)
                load_url = load_domain + load_data
                
                soup = bs(requests.get(load_url).text,"lxml")
                page_user_num = len(soup.select('.display-name-link'))
                for j in range(page_user_num):
                    user_account = soup.select('.display-name-link > a')[j].text
                    if not user_account in watch_dict:
                        watch_dict[user_account] = set([en_title])
                        user_list.append(user_account)
                    else:
                        watch_dict[user_account].update([en_title])
                        
            except:
                print('%s: no loads'%imdb_id)
                break
        
    
    except:
        traceback.print_exc(limit=1, file=sys.stdout)
        time.sleep(RETRYTIME)
        
    print("-----------------------------")
    print('movie_list: %s'%movie_list)
    print('watch_dict: %s'%watch_dict)
    print('user_list: %s'%user_list)
    print('review_num: %s'%review_num)
    print('len(user_list): %d'%len(user_list))


# multithread crawler
'''
with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERNUM) as executor:
    for search_title in re_en_list:
        #executor.map(worker,search_title)
'''

futures = []
threads = ThreadPoolExecutor(WORKERNUM)

for imdb_id in id_list:
    futures.append(threads.submit(worker,imdb_id))
wait(futures)

#csvfile.flush()
#csvfile.close()

tEnd = time.time()
print("-----------------------------")
#print("Getting data num: %s"%(len(nmbio_df)))
print("Concurrent worker num: %s"%(WORKERNUM))
print("Execute time: %s"%(tEnd-tStart))

