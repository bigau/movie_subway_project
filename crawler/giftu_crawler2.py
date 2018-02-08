
# coding: utf-8

# In[6]:


import re
import json
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime


today = time.strftime("%Y%m%d", time.localtime())


def cate_crawler(cate_key):
    cate_url = "https://www.giftu.com.tw/ws_GetProdItemList.asmx/ShowClassSub"
    form_data = {'ClassSubId': int(cate_key.split("-")[0])}
    r = requests.post(cate_url, data=form_data)
    prod_DOMAIN = "http://www.giftu.com.tw/Product.aspx?"
    prod_urls = [prod_DOMAIN + x.replace("amp;", "") for x in re.findall('ProdId=\d+&amp;ProdItemId=\d+', r.text)]
    cate_dict[cate_key].extend(prod_urls)
    


def prod_crawler(prod_url, cate_value):

    resp = requests.get(prod_url)
    soup = BeautifulSoup(resp.text, 'html5lib')
    prod_dict = {}
    prod_dict['ID'] = 'gt' + soup.select('small')[1].text.replace("品號：", "").replace(".", "").zfill(6)
    prod_dict['category'] = cate_value
    prod_dict['href'] = prod_url
    prod_dict['name'] = soup.select('.pricetitle')[0].text
    prod_dict['price'] = soup.select('.s_price')[0].text.replace(",", "").split()[1]
    prod_dict['brand'] = [soup.select('small')[0].text + "。" + soup.select('div.writing > p')[1].text]
    prod_dict['desc'] = [soup.select('p')[0].text + soup.select('div.writing > p')[0].text]
    prod_dict['memo'] = soup.select('p')[1].text

    try:
        errorChk = "first error"
        url = "https://www.giftu.com.tw/ws_prod.asmx/ShowReply"
        resps = requests.get(url)
        comment_list = re.findall('"ds-text"&gt;(.+?)&', resps.text.replace("\n", ""))
        errorChk = "second error"
        button_url = 'https://www.giftu.com.tw/' + re.findall('"khs-btn" href="(.*)"&', resps.text)[0]
        response = requests.get(button_url)
        s = BeautifulSoup(response.text, 'html5lib')

        name = s.select('.ds-name')
        for i in range(len(name)):
            text_list = s.select('.ds-text')[i].text
            comment_list.append(text_list)
        prod_dict['comment'] = comment_list
    except:
        print(errorChk)


    p_list = ["https://www.giftu.com.tw" + soup.select('#Main_imgProduct')[0]['src']]
    i = 0
    while True:
        try:
            p_list.append(soup.select('.imgfancybox > img')[i]['src'])
            i += 1
        except IndexError:
            break
    prod_dict['picture'] = p_list
    content_list.append(prod_dict)
    print(prod_dict["name"])



if __name__ == "__main__":
    
    cate_dict = {
        '1-餐具廚具':[],
        '2-傢俱飾品':[],
        '11-書寫工具':[],
        '12-辦公用品':[],
        '13-個人配件':[],
        '24-首飾':[],
        '15-玩偶':[],
        '16-卡通經典':[]
    }
    for cate_key in cate_dict.keys():
        cate_crawler(cate_key)
        print(cate_key + " urls list done")
    

    numThread = 10
    threads = ThreadPoolExecutor(numThread)
    futures = []
    thStart = datetime.now()

    with ThreadPoolExecutor(max_workers=numThread) as executor:
    
        for cate_key in cate_dict.keys():
            cate_value = int(cate_key.split("-")[0])
            content_list = []
            for url in cate_dict[cate_key]:
                futures.append(threads.submit(prod_crawler, url, cate_value))
            
            with open('gt_prod_%s_%s.json' % (cate_value, today), 'w') as f:
                f.write(json.dumps(content_list, ensure_ascii=False, indent=4))
            print(cate_key + " done")

        
    wait(futures)
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
        
    print("執行緒:" + str(numThread))
    
    prod_num = ""
    for cate_key in cate_dict.keys():
        prod_num += len(cate_dict[cate_key])
        
    print("商品數:" + str(prod_num))
    print("耗時:" + timeSpent)

