from pyparsing import col
import streamlit as st
import requests
import pandas as pd
import bs4
import os
import re
import streamlit.components.v1 as components
from st_aggrid import AgGrid
import base64

st.set_page_config(page_title='爬取当当网的热门书籍',page_icon='book',layout='wide')


def get_dangdang(page):
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page)
    header = {"User-Agent":"BaiduSpider"}
    return requests.get(url,header).text

def get_onepage_info(soup):
    rank = []
    rank_tags = soup.find_all("div",class_="list_num" )
    for rank_tag in rank_tags:
        rank.append(rank_tag.string)

    title = []
    title_tags = soup.find_all("img",attrs={"title":re.compile(".?")})
    for title_tag in title_tags:
        title.append(title_tag["title"])

    author = []
    author_tags = soup.find_all("div", class_="publisher_info")
    for i in range(0,len(author_tags),2):
        try:
            author.append(author_tags[i].a["title"])
        except:
            author.append('无')

    recommend = []
    recommend_tags = soup.find_all("span", class_="tuijian")
    for recommend_tag in recommend_tags:
        recommend.append(recommend_tag.string)

    publisher = []
    publisher_tags = soup.find_all("div", class_="publisher_info")
    for i in range(1,len(publisher_tags),2):
        publisher.append(publisher_tags[i].a.string)
        
    price = []
    all_price_tags = soup.find_all("div", class_="price")
    for all_price_tag in all_price_tags:
        price.append(all_price_tag.find('span',class_='price_n').string)
    
    
    return pd.DataFrame({"rank":rank,
              "title":title,
             'author':author,
             'recommend':recommend,
             'publisher':publisher,
             'price':price})

def main(page):
    html_doc = get_dangdang(page)
    soup = bs4.BeautifulSoup(html_doc)
    return get_onepage_info(soup)



components.html('<h1><center>当当网热门数据数据爬取</center></h1>')

"""- 看看要爬取的网页是什么样子的吧"""

""""""
checkbox = st.checkbox('显示网页')
if checkbox:
    components.iframe('http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-1',height=1000,width=1200,scrolling=True)

""""""
"""- 参数展示"""
info = """
爬虫使用的包:`requests`\n
解析使用的包:`bs4`\n
网址: http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-1\n
请求头:{"User-Agent":"BaiduSpider"}\n
"""
st.info(info)
col1, col2, col3 = st.columns([1,1,1])
data = []
with col1:
    page = st.number_input('要爬取多少页呢?(最多25页)',min_value=1,max_value=25)
    
with col2:
    "准备好了吗,点击:"
    button = st.button('开始爬取!')

with col3:
    if button:
        st.snow()
        if len(data)<=0:
            info = '开始爬取...'
            st.info(info)
        
        data = pd.concat([main(i) for i in range(1,page+1)])
        st.success('爬取成功!')
    else:
        st.warning('你还没有开始爬取呢!')
if len(data)>0:
    AgGrid(data)
else:
    with open("./resources/gif1.gif", "rb") as f:
        contents = f.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        st.markdown(
        f'<center><img src="data:image/gif;base64,{data_url}" alt="cat gif"></center>',
        unsafe_allow_html=True
        )

if len(data)>0:
    st.download_button('下载数据集',data.to_csv().encode('utf-8'),mime='text/csv')
    

components.html('<h1><center>爬虫源码展示</center></h1>')

"""
```python
import requests
import bs4
import re
import pandas as pd
import os


def get_dangdang(page):
    url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-" + str(page)
    header = {"User-Agent":"BaiduSpider"}
    return requests.get(url,header).text

def get_onepage_info(soup):
    rank = []
    rank_tags = soup.find_all("div",class_="list_num" )
    for rank_tag in rank_tags:
        rank.append(rank_tag.string)

    title = []
    title_tags = soup.find_all("img",attrs={"title":re.compile(".?")})
    for title_tag in title_tags:
        title.append(title_tag["title"])

    author = []
    author_tags = soup.find_all("div", class_="publisher_info")
    for i in range(0,len(author_tags),2):
        try:
            author.append(author_tags[i].a["title"])
        except:
            author.append('无')

    recommend = []
    recommend_tags = soup.find_all("span", class_="tuijian")
    for recommend_tag in recommend_tags:
        recommend.append(recommend_tag.string)

    publisher = []
    publisher_tags = soup.find_all("div", class_="publisher_info")
    for i in range(1,len(publisher_tags),2):
        publisher.append(publisher_tags[i].a.string)
        
    price = []
    all_price_tags = soup.find_all("div", class_="price")
    for all_price_tag in all_price_tags:
        price.append(all_price_tag.find('span',class_='price_n').string)
    
    
    return pd.DataFrame({"rank":rank,
              "title":title,
             'author':author,
             'recommend':recommend,
             'publisher':publisher,
             'price':price})

def main(page):
    html_doc = get_dangdang(page)
    soup = bs4.BeautifulSoup(html_doc)
    return get_onepage_info(soup)

if __name__ == "__main__":
    data = pd.concat([main(i) for i in range(1,26)]).reset_index().drop(columns='index')
    if not os.path.exists('./results'):
        os.mkdir('./results')
    else:
        data.to_excel('./results/data.xlsx',index=False)
```
"""







