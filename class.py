#coding=utf-8
import time
import sys 
import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os
import random
import subprocess
import re

reload(sys)
sys.setdefaultencoding('utf-8')
print "正在搜索公众号：", sys.argv[1]
wechat_id = sys.argv[1]

if not os.path.exists(wechat_id):
        os.makedirs(wechat_id) ##创建一个存放文件夹
os.chdir(wechat_id) ##切换到上面创建的文件夹

user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",

    ]
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）




class crawler:
    def __init__(self):
        self.article = [];
        self.page = [];

    def get_page(self,wid):
        page_url = wid 
        print "开始爬取页面：", page_url
        time.sleep(1.6)
        start_html = requests.get(page_url,  headers={'User-Agent': user_agent_list[random.randint(0,19)]}) 
        start_html.encoding = 'utf-8'
        Soup = BeautifulSoup(start_html.text, 'lxml')
        article_list = Soup.find_all('a',class_="question_link")
        page_list = Soup.select(".w4_5 > span > a")

        new_page_list = []
        new_article_list = []


        for page in page_list:
            page_url = "http://chuansong.me"+page['href']
            if page_url not in self.page:
                self.page.append(page_url)
                self.get_page(page_url)

        for article in article_list:
            article_url = "http://chuansong.me"+article['href']
            # self.article.append(article_url)
            self.get_article(article_url)

    def get_article(self,article_url):
        time.sleep(1.7)
        article_page = requests.get(article_url,  headers={'User-Agent': user_agent_list[random.randint(0,17)]})  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
        Soup = BeautifulSoup(article_page.text, 'lxml') ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）

        article_text = Soup.select(".rich_media_content p") or Soup.select(".page-content p") #.find_all('img')  ##find('div', class_='container').
        date = Soup.select("#post-date")[0].get_text().strip()
        name = Soup.select("#activity-name")[0].get_text().strip()
        name = re.sub("\/", " ", name, count=0, flags=0)
        if not os.path.isfile(date+" "+name+".md"):
            print date+name
            with open(date+" "+name+".md", 'a') as f:
                f.write("title: "+name+"\n")
                f.write("date: "+date+"\n")
                f.write("tags: 杂的文"+"\n")
                f.write("---")
                f.write('\n')
                # f.write(date)
                # f.write('\n')
                for p in article_text:
                    text=p.get_text()
                    f.write(text)
                    f.write('\n')


c = crawler()
c.get_page("http://chuansong.me/account/" + wechat_id)

