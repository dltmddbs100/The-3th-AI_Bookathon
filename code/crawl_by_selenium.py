import numpy as np
import pandas as pd
import random
from tqdm.notebook import tqdm

import re
import time
import warnings
warnings.filterwarnings('ignore')

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# setting chrome driver
def chrome_setting():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('chromedriver', options=chrome_options)
  return driver

def contain(data=None,column='contents',regex=None):
  return data[data[column].str.contains(regex)][column]


# 신춘문예작
## 동아일보

driver=chrome_setting()
title=[]
content=[]

for i in tqdm(range(0,10)):
  driver.get('https://www.donga.com/docs/sinchoon/')
  time.sleep(0.1)
  driver.find_element_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]/a['+str(22-i)+']/font').click()
  time.sleep(0.1)
  try:
    driver.find_element_by_xpath('/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/a/img').click()
    time.sleep(0.1)
    target_present = EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td'))
    text=WebDriverWait(driver, 5).until(target_present).text
    tit=re.split('\n{2,}',text)[0]
    con=re.split('\n{2,}',text)[1:]
    con=' '.join(con)

    title.append(tit) 
    content.append(con)
  except:
    continue

for i in tqdm(range(0,12)):
  driver.get('https://www.donga.com/docs/sinchoon/'+str(2010+i)+'/02_1.html')
  time.sleep(0.1)
  target_present = EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td'))
  text=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)
  tit=re.split('\n{2,}',text)[0]
  con=re.split('\n{2,}',text)[1]
  
  
  title.append(tit) 
  content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})
for i in range(a.shape[0]):
  a['title'][i]=re.sub(' +',' ',a['title'][i])
  a['title'][i]=re.sub('\u3000',' ',a['title'][i])
  a['title'][i]=re.sub('\n','',a['title'][i])

  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])

a['refer']='동아일보'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_동아일보_소설.csv',index=False)


## 경향신문
book_lists=['https://www.khan.co.kr/culture/book/article/200812311640185',
            'https://www.khan.co.kr/culture/book/article/200912311708595',
            'https://www.khan.co.kr/culture/book/article/201712312051005',
            'https://www.khan.co.kr/culture/book/article/201812312107005',
            'https://www.khan.co.kr/culture/book/article/201912312100005',
            'https://www.khan.co.kr/culture/book/article/202012311940005',
            'https://www.khan.co.kr/culture/book/article/201012311418085',
            'https://www.khan.co.kr/culture/book/article/201201012012425',
            'https://www.khan.co.kr/culture/book/article/201212312200165',
            'https://www.khan.co.kr/culture/book/article/201412312035145',
            'https://www.khan.co.kr/culture/book/article/201512312005295',
            'https://www.khan.co.kr/culture/book/article/201701012126005',
            'https://www.khan.co.kr/culture/book/article/200301021050461',
            'https://www.khan.co.kr/culture/book/article/200301021051211',
            'https://www.khan.co.kr/culture/book/article/200312311654071',
            'https://www.khan.co.kr/culture/book/article/200312311648021',
            'https://www.khan.co.kr/culture/book/article/200312311646241',
            'https://www.khan.co.kr/culture/book/article/200312311644531',
            'https://www.khan.co.kr/culture/book/article/200501031719171',
            'https://www.khan.co.kr/culture/book/article/200501031721211']

driver=chrome_setting()
title=[]
content=[]

for i in tqdm(book_lists):
  driver.get(i)
  time.sleep(0.1)
  tit=driver.find_element_by_xpath('//*[@id="article_title"]').text
  time.sleep(0.1)
  
  target_present = EC.presence_of_element_located((By.XPATH, '//*[@id="articleBody"]'))
  con=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)    
  
  title.append(tit) 
  content.append(con)


# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})
a=a.drop_duplicates()

for i in range(a.shape[0]):
  try:
    a['title'][i]=re.split('-',a['title'][i])[1]
  except:
    pass
  a['title'][i]=re.sub(' +',' ',a['title'][i])
  a['title'][i]=re.sub('\n','',a['title'][i])

  a['contents'][i]=re.sub('(일러스트 *\| *.+ *(기자|작가|))|일러스트','',a['contents'][i])
  a['contents'][i]=re.sub('〈끝〉|〈계속〉','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])

a['refer']='경향신문'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_경향신문_소설.csv',index=False)


## 경인일보
url_list=['http://m.kyeongin.com/view.php?key=20210104010006543',
          'http://m.kyeongin.com/view.php?key=20201228010005655',
          'http://m.kyeongin.com/view.php?key=20200102010000302',
          'http://m.kyeongin.com/view.php?key=20200102010000301',
          'http://m.kyeongin.com/view.php?key=20190102010000225',
          'http://m.kyeongin.com/view.php?key=20190102010000227',
          'http://m.kyeongin.com/view.php?key=20180102010000269',
          'http://m.kyeongin.com/view.php?key=20170102010008975',
          'http://m.kyeongin.com/view.php?key=20151222010008277',
          'http://m.kyeongin.com/view.php?key=930655',
          'http://m.kyeongin.com/view.php?key=797388',
          'http://m.kyeongin.com/view.php?key=701759',
          'http://m.kyeongin.com/view.php?key=626188',
          'http://m.kyeongin.com/view.php?key=559550',
          'http://m.kyeongin.com/view.php?key=494569',
          'http://m.kyeongin.com/view.php?key=411235',
          'http://m.kyeongin.com/view.php?key=360180',
          'http://m.kyeongin.com/view.php?key=313776',
          'http://m.kyeongin.com/view.php?key=288414']

driver=chrome_setting()
title=[]
content=[]

for i in tqdm(url_list):
  driver.get(i)
  time.sleep(0.1)
  tit=driver.find_element_by_xpath('//*[@id="container"]/div[1]/div/div/span').text
  time.sleep(0.1)
  
  target_present = EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]'))
  con=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)    
  
  title.append(tit) 
  content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

for i in range(a.shape[0]):
  a['contents'][i]=re.sub('(일러스트 *\/ *.{3} *(기자|작가|))|일러스트','',a['contents'][i])
  a['contents'][i]=re.sub('\[경인일보=\]','',a['contents'][i])
  a['contents'][i]=re.sub('(■ 소설 당선작 : )|▲','',a['contents'][i])
  a['contents'][i]=re.sub('(→ 계속)|(<끝>)','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub(r'\\',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='경인일보'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_경인일보_소설.csv',index=False)


## 중앙 신인문학상
url_list=['https://www.joongang.co.kr/article/4137800#home',
          'https://www.joongang.co.kr/article/4137870#home',
          'https://www.joongang.co.kr/article/4137873#home',
          'https://www.joongang.co.kr/article/4347769#home',
          'https://www.joongang.co.kr/article/4347782#home',
          'https://www.joongang.co.kr/article/4347781#home',
          'https://www.joongang.co.kr/article/230336#home',
          'https://www.joongang.co.kr/article/392571#home',
          'https://www.joongang.co.kr/article/1683745#home',
          'https://www.joongang.co.kr/article/3301705#home',
          'https://www.joongang.co.kr/article/3781019#home',
          'https://www.joongang.co.kr/article/4467443#home',
          'https://www.joongang.co.kr/article/6217083#home',
          'https://www.joongang.co.kr/article/9365008#home',
          'https://www.joongang.co.kr/article/12654649#home',
          'https://www.joongang.co.kr/article/15875572#home',
          'https://www.joongang.co.kr/article/20625031#home',
          'https://www.joongang.co.kr/article/21966681#home',
          'https://www.joongang.co.kr/article/22992634#home']

driver=chrome_setting()

title=[]
content=[]

for i in tqdm(url_list):
  driver.get(i)
  time.sleep(0.1)
  tit=driver.find_element_by_xpath('//*[@id="container"]/section/article/header/h1').text
  time.sleep(0.1)
  
  target_present = EC.presence_of_element_located((By.XPATH, '//*[@id="article_body"]'))
  con=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)    
  
  title.append(tit) 
  content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

for i in range(a.shape[0]):
  a['contents'][i]=re.sub('(\[일러스트 *= *.{2} .{3}\])|(\[*일러스트 *= *.{3}\]*)',' ',a['contents'][i])
  a['contents'][i]=re.sub('\nADVERTISEMENT\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('(\[*그림 *= *.{2} .{3}\]*)|(\[*그림 *= *.{3}\]*)|(▶ *그림 *= *.{3})','',a['contents'][i])
  a['contents'][i]=re.sub('(→ 계속)|(-끝-)','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('\*',' ',a['contents'][i])
  a['contents'][i]=re.sub(r'\\',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='중앙신인문학상'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_중앙신인문학상_소설.csv',index=False)


## 세계일보
driver=chrome_setting()
title=[]
content=[]

for i in tqdm(range(0,21)):
  if i<10:
    url='http://shinchun.segye.com/shinchun/shinchun_200'+str(i)+'_story_j.asp?gb=1'
  else:
    url='http://shinchun.segye.com/shinchun/shinchun_20'+str(i)+'_story_j.asp?gb=1'
  
  driver.get(url)
  time.sleep(0.1)
  tit=driver.find_element_by_xpath('/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[3]/table/tbody/tr[3]/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]').text
  time.sleep(0.1)
  
  target_present = EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td[1]/table/tbody/tr[1]/td[3]/table/tbody/tr[3]/td'))
  con=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)    
  
  title.append(tit) 
  content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

for i in range(a.shape[0]):
  if len(a['contents'][i].split(':'))!=3:
    a['contents'][i]=':'.join(a['contents'][i].split(':')[2:])
  else:
    a['contents'][i]=a['contents'][i].split(':')[2]

for i in range(a.shape[0]):
  a['contents'][i]=re.sub('(그림 *= *.{3}\(* *화가 *\)*\n)|(그림 *= *.{3})\n','',a['contents'][i])
  a['contents'][i]=re.sub('<끝>|〈끝〉','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('\*',' ',a['contents'][i])
  a['contents'][i]=re.sub(r'\\',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='세계일보'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_세계일보_소설.csv',index=False)


## 서울신문
url_list=['https://www.seoul.co.kr/news/newsView.php?id=20210101029002',
          'https://www.seoul.co.kr/news/newsView.php?id=20200102040001',
          'https://www.seoul.co.kr/news/newsView.php?id=20190101029004',
          'https://www.seoul.co.kr/news/newsView.php?id=20180101029001',
          'https://www.seoul.co.kr/news/newsView.php?id=20170102033003',
          'https://www.seoul.co.kr/news/newsView.php?id=20160101033003',
          'https://www.seoul.co.kr/news/newsView.php?id=20150101033005',
          'https://www.seoul.co.kr/news/newsView.php?id=20140101034001',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=98&user=webmaster&bid=sinchun&key=subject&word=2013',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=94&user=webmaster&bid=sinchun&key=subject&word=2012',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=86&user=webmaster&bid=sinchun&key=subject&word=2011',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=80&user=webmaster&bid=sinchun&key=subject&word=2010',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=73&user=webmaster&bid=sinchun&key=subject&word=2009',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=67&user=webmaster&bid=sinchun&key=subject&word=2008',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=61&user=webmaster&bid=sinchun&key=subject&word=2007',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=55&user=webmaster&bid=sinchun&key=subject&word=2006',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=49&user=webmaster&bid=sinchun&key=subject&word=2005',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=45&user=webmaster&bid=sinchun&key=subject&word=2004',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=39&user=webmaster&bid=sinchun&key=subject&word=2003',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=33&user=&bid=sinchun&key=subject&word=2002',
          'https://nownews.seoul.co.kr/board/board.php?job=view&no=27&user=&bid=sinchun&key=subject&word=2001']

driver=chrome_setting()
title=[]
content=[]

for i in tqdm(url_list):
  if int(i[-4:]) in range(2001,2014):
    driver.get(i)
    time.sleep(0.1)
    tit=driver.find_element_by_xpath('/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/p[1]/table/tbody/tr/td/table[2]/tbody/tr[1]/td/strong').text
    time.sleep(0.1)
    
    target_present = EC.presence_of_element_located((By.XPATH, '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/p[1]/table/tbody/tr/td/table[2]/tbody/tr[3]/td'))
    con=WebDriverWait(driver, 5).until(target_present).text
    time.sleep(0.1)    
    
    title.append(tit) 
    content.append(con)
  else:
    driver.get(i)
    time.sleep(0.1)
    tit=driver.find_element_by_xpath('//*[@id="viewWrapDiv"]/div[2]/div[2]/h1').text
    time.sleep(0.1)
    
    target_present = EC.presence_of_element_located((By.XPATH, '//*[@id="atic_txt1"]'))
    con=WebDriverWait(driver, 5).until(target_present).text
    time.sleep(0.1)    
    
    title.append(tit) 
    content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

for i in range(a.shape[0]):
  a['contents'][i]=re.sub('▲ *일러스트 *.{3} *기자','',a['contents'][i])
  a['contents'][i]=re.sub('[a-z]+@[a-z]+\.[a-z]+.[a-z]*','',a['contents'][i])
  a['contents'][i]=re.sub('\(끝\)','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('\*',' ',a['contents'][i])
  a['contents'][i]=re.sub(r'\\',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='서울신문'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_서울신문_소설.csv',index=False)


## 조선일보
url_list=['https://www.chosun.com/site/data/html_dir/2002/12/31/2002123170181.html',
          'https://www.chosun.com/site/data/html_dir/2002/12/31/2002123170182.html',
          'https://www.chosun.com/site/data/html_dir/2003/12/31/2003123170321.html',
          'https://www.chosun.com/site/data/html_dir/2004/12/31/2004123170281.html',
          'https://www.chosun.com/site/data/html_dir/2006/12/31/2006123100487.html',
          'https://www.chosun.com/site/data/html_dir/2007/12/31/2007123100946.html',
          'https://www.chosun.com/site/data/html_dir/2008/12/31/2008123101211.html',
          'https://www.chosun.com/site/data/html_dir/2009/12/31/2009123102271.html',
          'https://www.chosun.com/site/data/html_dir/2010/12/31/2010123100790.html',
          'https://www.chosun.com/site/data/html_dir/2011/12/30/2011123001234.html',
          'https://www.chosun.com/site/data/html_dir/2012/12/31/2012123100998.html',
          'https://www.chosun.com/site/data/html_dir/2015/12/31/2015123101388.html',
          'https://www.chosun.com/site/data/html_dir/2017/01/01/2017010100681.html',
          'https://www.chosun.com/site/data/html_dir/2017/12/31/2017123100707.html',
          'https://www.chosun.com/site/data/html_dir/2018/12/31/2018123101284.html',
          'https://www.chosun.com/site/data/html_dir/2019/12/31/2019123101415.html',
          'https://www.chosun.com/culture-life/2021/01/01/QSZ6OISPRRCITHQ2UAJS4SYGMQ/']

driver=chrome_setting()
title=[]
content=[]

for i in tqdm(url_list):
  driver.get(i)
  time.sleep(0.1)
  tit=driver.find_element_by_xpath('//*[@id="fusion-app"]/div[1]/div[2]/div/div/div[3]/h1/span').text
  time.sleep(0.1)
  
  target_present = EC.presence_of_element_located((By.XPATH, '//*[@id="fusion-app"]/div[1]/div[2]/div/section/article/section'))
  con=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)    
  
  title.append(tit) 
  content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

for i in range(a.shape[0]):
  a['contents'][i]=re.sub('(일러스트 *= *.{2,3}\n)|(그림 *= *.{2,3}\n)',' ',a['contents'][i])
  a['contents'][i]=re.sub('〈CAM .{3}〉','',a['contents'][i])
  a['contents'][i]=re.sub('〈끝〉|<끝>|\(끝\)|','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('\*',' ',a['contents'][i])
  a['contents'][i]=re.sub(r'\\',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='조선일보'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예당선작/신춘_조선일보_소설.csv',index=False)


## 문화일보
url_list=['http://www.munhwa.com/news/view.html?no=20050101010349300730010',
          'http://www.munhwa.com/news/view.html?no=2005010101035030073001',
          'http://www.munhwa.com/news/view.html?no=2006010201014730136007',
          'http://www.munhwa.com/news/view.html?no=2006122901034730136002',
          'http://www.munhwa.com/news/view.html?no=2008010101035430008002',
          'http://www.munhwa.com/news/view.html?no=20090101010354300230060',
          'http://www.munhwa.com/news/view.html?no=2010010101036230023005',
          'http://www.munhwa.com/news/view.html?no=20110101010355300650010',
          'http://www.munhwa.com/news/view.html?no=2012010101035502202003',
          'http://www.munhwa.com/news/view.html?no=20130102010342300650030',
          'http://www.munhwa.com/news/view.html?no=2014010201033430065003',
          'http://www.munhwa.com/news/view.html?no=2015010201034212000001',
          'http://www.munhwa.com/news/view.html?no=2016010401033412000001',
          'http://www.munhwa.com/news/view.html?no=2017010201033412000001',
          'http://www.munhwa.com/news/view.html?no=2018010201033412000001',
          'http://www.munhwa.com/news/view.html?no=2019010201034212000001',
          'http://www.munhwa.com/news/view.html?no=2020010201033412000001',
          'http://www.munhwa.com/news/view.html?no=2021010401032712000001']

driver=chrome_setting()
title=[]
content=[]

for i in tqdm(url_list):
  driver.get(i)
  time.sleep(0.1)
  tit=driver.find_element_by_xpath('/html/body/div[1]/table[5]/tbody/tr/td[1]/table[6]/tbody/tr/td/table[3]/tbody/tr/td/span').text
  time.sleep(0.1)
  
  target_present = EC.presence_of_element_located((By.XPATH, '//*[@id="NewsAdContent"]'))
  con=WebDriverWait(driver, 5).until(target_present).text
  time.sleep(0.1)    
  
  title.append(tit) 
  content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

for i in range(a.shape[0]):
  a['contents'][i]=re.sub('(일러스트 *= *.{2,3} .{2}[ \n]+)|(일러스트 *= *.{2,3})',' ',a['contents'][i])
  a['contents'][i]=re.sub('▲|■',' ',a['contents'][i])
  a['contents'][i]=re.sub('[a-z0-9]+@',' ',a['contents'][i])
  a['contents'][i]=re.sub('〈끝〉|<끝>|\(끝\)|-끝-|＜ *끝 *＞|〈 *끝 *〉','',a['contents'][i])

  a['contents'][i]=re.sub('…+','…',a['contents'][i])
  a['contents'][i]=re.sub('(\n)+','\n',a['contents'][i])
  a['contents'][i]=re.sub('\n',' ',a['contents'][i])
  a['contents'][i]=re.sub('\*',' ',a['contents'][i])
  a['contents'][i]=re.sub(r'\\',' ',a['contents'][i])
  a['contents'][i]=re.sub('．','. ',a['contents'][i])
  a['contents'][i]=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='문화일보'
a['types']='단편소설'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/신춘문예 당선작/신춘_문화일보_소설.csv',index=False)


# 한국산문 작가협회
driver=chrome_setting()
title=[]
content=[]

for i in tqdm(range(1,27)):
  driver.get('http://koreaessay.com/bbs/board.php?bo_table=hs_supilgongmo&page=8&page='+str(i))
  time.sleep(0.1)

  for j in range(0,15):
    tit=driver.find_element_by_xpath('//*[@id="js_view"]/tbody/tr[2]/td/form/table/tbody/tr['+str(j+3)+']/td[2]/nobr/a[1]').text
    
    if '수정'in tit:
      pass
    else:
      time.sleep(0.1)
      driver.find_element_by_xpath('//*[@id="js_view"]/tbody/tr[2]/td/form/table/tbody/tr['+str(j+3)+']/td[2]/nobr/a[1]').click()
      
      con=driver.find_element_by_xpath('//*[@id="writeContents"]').text  
      driver.back()

      title.append(tit) 
      content.append(con)

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})
a=a.drop(contain(a,'title',regex='응모|@').index).reset_index(drop=True)

for i in range(a.shape[0]):
  a.at[i,'contents']=re.sub('\d{4}\. *\d{1,2}\. *\d{1,2}\.*',' ',a['contents'][i])

  a.at[i,'contents']=a['contents'][i].replace('\u200b','').replace('\xa0','').replace('\ufeff','').replace('\u3000','') # 유니코드 제거
  a.at[i,'contents']=re.sub('\([^\(\)]+\)|\[.+\]',' ',a['contents'][i]) # (), [] 안의 내용제거
  a.at[i,'contents']=re.sub('(\. *\. *\.)+|…+|ㆍ{3,}|·{3,}','…',a['contents'][i]) # ...대체
  a.at[i,'contents']=re.sub('_|\*|\+|─|=|\^|;',' ',a['contents'][i]) # 특수기호 제거
  a.at[i,'contents']=re.sub('-+|—+','-',a['contents'][i]) # --- 대체
  a.at[i,'contents']=re.sub('[ㄱ-ㅎㅏ-ㅣ]+',' ',a['contents'][i]) # 자모음 제거
  a.at[i,'contents']=re.sub('[一-龥]',' ',a['contents'][i]) # 한자제거
  a.at[i,'contents']=re.sub('!+','!',a['contents'][i]) # ! 중복제거
  a.at[i,'contents']=re.sub('\?+','?',a['contents'][i]) # ? 중복제거
  a.at[i,'contents']=re.sub('~+','~',a['contents'][i]) # ~ 중복제거

  a.at[i,'contents']=re.sub('(\n)+','\n',a['contents'][i])
  a.at[i,'contents']=re.sub('\n',' ',a['contents'][i])
  a.at[i,'contents']=re.sub(r'\\',' ',a['contents'][i])
  a.at[i,'contents']=re.sub('．','. ',a['contents'][i])
  a.at[i,'contents']=re.sub(' +',' ',a['contents'][i])
  a['contents'][i]=a['contents'][i].strip()

a['refer']='산문작가협회'
a['types']='수필공모'

a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/산문작가협회/산문작가협회_수필공모.csv',index=False)


# 재미수필 문학가협회
driver=chrome_setting()

driver.get('http://jaemisupil.com/recommend_articles/648')
content=driver.find_element_by_xpath('//*[@id="body_container"]/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div/div[1]').text

title=re.findall('\n {2,6}\d{1,2}\. *[\S ]+\n',content)
contents=re.split('\n {2,6}\d{1,2}\. *[\S ]+\n',content)[1:]

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':contents})
a['refer']='재미수필 문학가협회'
a['types']='반숙자_수필'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/재미수필 문학가협회/반숙자_수필_80선.csv',index=False)


# 수필.net
driver=chrome_setting()
title=[]
content=[]

for i in tqdm(range(1,58)):
  driver.get('http://supil.net/bbs/zboard.php?id=supil&page='+str(i)+'&select_arrange=headnum&desc=asc&category=&sn=off&ss=on&sc=on&keyword=&sn1=&divpage=1')

  for j in range(1,16) :
    time.sleep(0.1)
    try:
      tit=driver.find_element_by_xpath('/html/body/div/table[3]/tbody/tr['+str(2*j)+']/td[3]/a').text

      driver.find_element_by_xpath('/html/body/div/table[3]/tbody/tr['+str(2*j)+']/td[3]/a').click()
      time.sleep(0.1)

      con=driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/table/tbody/tr/td').text
      driver.back()

      content.append(con)
      title.append(tit)
    except:
      print('Page:', i)
      continue

# Parsing to DataFrame format and save
a=pd.DataFrame({'title':title,'contents':content})

a['refer']='수필_net_뜰'
a['types']='수필'
a=a[['refer','types','title','contents']]

a.to_csv('/content/drive/MyDrive/AI_Bookathon/Crawl_data/수필net/수필_net_뜰.csv',index=False)
