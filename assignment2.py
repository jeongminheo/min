from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


url = "https://book.naver.com/bestsell/bestseller_list.nhn"
book_list=[]
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)


# 네이버의 베스트셀러 웹페이지를 가져옵니다.
driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')



# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
book_page_urls = []
subject=[]
subject.insert(0,1)
for index in range(0, 10):

    dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
    link = dl_data.select('a')[0].get('href')
    book_page_urls.append(link)



# 메타 정보와 본문에서 필요한 정보를 추출합니다.
for index, book_page_url in enumerate(book_page_urls):

    driver.get(book_page_url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')


    title = bsObject.find('meta', {'property':'og:title'}).get('content')
    author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
    dd = bsObject.find('dt', text='가격').find_next_siblings('dd')[0]
    salePrice = dd.select('div.lowest strong')[0].text.replace('원','').replace(',','')
    originalPrice = dd.select('div.lowest span.price')[0].text.replace('원','').replace(',','')

    book_list.append([title,author,salePrice,originalPrice])

df=pd.DataFrame(np.array(book_list), columns=["title","author","salePrice","originalPrice"])
df.to_csv("C:\\Users\\min\\PycharmProjects\\pythonProject8\\book2",sep='\t')




