import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
from concurrent.futures import ThreadPoolExecutor




def logo():
    logos = r"""
     ____              _                               
    | __ ) _   _      / \   _ __ ___   ___ _ __   __ _ 
    |  _ \| | | |    / _ \ | '_ ` _ \ / _ \ '_ \ / _` |
    | |_) | |_| |   / ___ \| | | | | |  __/ | | | (_| |
    |____/ \__, |  /_/   \_\_| |_| |_|\___|_| |_|\__, |
            |___/                                 |___/ 
            
    @Github  : https://github.com/AmengDream
    @FileName: googlehacking.py                                      
    @Version : v1.0    
    """    
    sys.stdout.write(logos+"\n")

class Google:
    #构造函数
    def __init__(self):
        self.Google_txt = open('./Google.txt','a+')
        self.headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
    
    #请求页面
    def Request_html(self,search_q,page_stop):
        #谷歌镜像站，适合没有国外代理的用户，如果想要爬取Google官方数据，可以修改https://谷歌.mc-serve.cf/ 为 https://www.google.com/
        self.url = f"https://谷歌.mc-serve.cf/search?q={search_q}&start={page_stop}"         
        self.html = requests.get(url=self.url,headers=self.headers,timeout=5).text
    
    #解析页面   
    def Parse_html(self):
        soup = BeautifulSoup(self.html,features='lxml')
        div_tags = soup.find_all('div',class_='yuRUbf')
        
        #遍历第一个a标签的href值
        for div_tag in div_tags:
            a_tag = div_tag.find('a')
            if a_tag is not None:
                href_value = a_tag.get('href')
                self.Google_txt.write(href_value+'\n')
                print(f'[*]>>>{href_value}写入完成!!')
    
    def run(self,search_q,page_stop):
        self.Request_html(search_q,page_stop)
        self.Parse_html()    
    
if __name__ == '__main__':
    logo()
    
    google = Google()
    #hacking语法
    text = 'inurl:php?id='
    search_q = quote(text)
    #爬取页数,修改为你要爬取的页数
    page_stop = 10   
    #设置线程池，控制线程数为1
    pool = ThreadPoolExecutor(1)
    threads = []
    
    #循环爬取
    for page in range(page_stop):
        page *= 10
        thread = pool.submit(google.run,search_q,page)
        #防止被ban
        time.sleep(3)
        
     # 等待所有线程执行完成
    for thread in threads:
        thread.result()

    # 关闭线程池
    pool.shutdown()
    
    print('结果已写入Goole.txt文件')