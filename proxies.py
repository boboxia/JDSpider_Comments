# *-* coding:utf-8 *-*  
import requests  
from bs4 import BeautifulSoup  
import lxml  
from multiprocessing import Process, Queue  
import random  
import json  
import time  
import requests  
import telnetlib
  
class Proxies(object):  
  
  
    """docstring for Proxies"""  
    def __init__(self, page=3):  
        self.proxies = []  
        self.verify_pro = []  
        self.page = page  
        self.headers = {  
        'Accept': '*/*',  
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',  
        'Accept-Encoding': 'gzip, deflate, sdch',  
        'Accept-Language': 'zh-CN,zh;q=0.8'  
        }  
        self.get_proxies_nt()
        self.get_proxies_nn()  
  
    def get_proxies_nt(self):
        page = random.randint(1,10)  
        page_stop = page + self.page  
        while page < page_stop:  
            url = 'http://www.xicidaili.com/nt/%d' % page  
            html = requests.get(url, headers=self.headers).content  
            soup = BeautifulSoup(html, 'lxml')  
            ip_list = soup.find(id='ip_list')  
            for odd in ip_list.find_all(class_='odd'):  
                protocol = odd.find_all('td')[5].get_text().lower()+'://'  
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))  
            page += 1  
  
    def get_proxies_nn(self):  
        page = random.randint(1,10)  
        page_stop = page + self.page  
        while page < page_stop:  
            url = 'http://www.xicidaili.com/nn/%d' % page  
            html = requests.get(url, headers=self.headers).content  
            soup = BeautifulSoup(html, 'lxml')  
            ip_list = soup.find(id='ip_list')  
            for odd in ip_list.find_all(class_='odd'):  
                protocol = odd.find_all('td')[5].get_text().lower() + '://'  
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))  
            page += 1  
  
    def verify_proxies(self):  
        # 没验证的代理  
        old_queue = Queue()  
        # 验证后的代理  
        new_queue = Queue()  
        print ('verify proxy........')  
        works = []  
        for _ in range(2):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue,new_queue)))  
        for work in works:  
            work.start()  
        for proxy in self.proxies:  
            old_queue.put(proxy)  
        for work in works:  
            old_queue.put(0)  
        for work in works:  
            work.join()  
        self.proxies = []  
        while 1:  
            try:  
                self.proxies.append(new_queue.get(timeout=1))  
            except:  
                break  
        print ('verify_proxies done!')  
  
  
    def verify_one_proxy(self, old_queue, new_queue):  
        while 1:  
            proxy = old_queue.get()  
            if proxy == 0:break  
            protocol = 'https' if 'https' in proxy else 'http'  
            proxies = {protocol: proxy}  
            http_or_https=proxy.strip().split(":")[0]
            proxy_ip=proxy.strip().split(":")[1].split("//")[1]
            print("proxy_ip:",proxy_ip)
            proxy_port=proxy.strip().split(":")[2]
            print("proxy_port:", proxy_port)
            try:  
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:  
                    print ('success link baidu %s' % proxy)  
                    try:
                        telnetlib.Telnet(proxy_ip, port=proxy_port, timeout=2.0)
                    except:
                        print('connect failure')
                        print ('fail %s' % proxy)
                    else:
                        print ('success link Telnet %s' % proxy)
                        new_queue.put(proxy)

                      
            except:  
                print ('fail %s' % proxy)  
  
  
if __name__ == '__main__':  
    a = Proxies()
    a.proxies=[]
    a.proxies = ["https://122.4.40.136:21982",
"https://180.116.151.84:43057",
"https://171.14.235.164:43086",
"https://106.110.197.135:30721",
"https://116.239.107.11:48377",
"https://123.149.162.225:30111",
"https://183.166.7.118:40882",
"https://117.29.192.204:22733",
"https://121.226.153.38:21253",
"https://183.166.86.96:47618",
"https://117.57.90.16:36547",
"https://123.54.252.66:25523",
"https://114.230.105.33:29878",
"https://117.69.50.64:23113",
"https://113.120.36.68:37302",
"https://114.228.138.67:39040",
"https://114.230.104.201:43237",
"https://1.198.13.192:24963",
"https://171.12.166.131:31377",
"https://183.154.50.61:36436"]
    a.verify_proxies()  
    print (a.proxies)  
    proxie = a.proxies   
    with open('proxies_success.txt', 'a') as f:
       for proxy in proxie:  
             f.write(proxy+'\n')
