import os
import xml.etree.ElementTree as ET 
import requests
import pandas as pd 

def parsing_tass_news():
    url = 'https://tass.ru/rss/v2.xml'
    a = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=a)
        root = ET.fromstring(response.content)
        news_items = []
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            if title and link:
                news_items.append({'title':title,'content':description,'link':link,'date':pub_date,'source_type':'website','source_name':'tass.ru'})
        return news_items
    except:
        return[]

df = 'tass_news(1.1).csv'
news = parsing_tass_news()
if len(news)>0:
    df1 = pd.DataFrame(news)
    if os.path.exists(df):
        df1.to_csv(df,mode='a',header=False,index=False,encoding='utf-8-sig')
    else:
        df1.to_csv(df,index=False,encoding='utf-8-sig')