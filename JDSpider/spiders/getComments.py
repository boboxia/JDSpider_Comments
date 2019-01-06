# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy_redis.spiders import RedisCrawlSpider
from JDSpider.items import JdspiderItem

class GetcommentsSpider(RedisCrawlSpider):
# class GetcommentsSpider(scrapy.Spider):
    name = "getComments"
    redis_key = 'getComments:start_urls'
    allowed_domains = ["jd.com"]
    # start_urls = ['https://www.jd.com/allSort.aspx']
    #lpush getComments:start_urls 'https://www.jd.com/allSort.aspx'

    def parse(self, response):


        if "list.jd.com" in str(response.url):
            yield scrapy.Request(url=response.url, callback=self.getGoodsUrl)
        elif "comment" in str(response.url):
            yield scrapy.Request(url=response.url, callback=self.getCommentsData)
        if "allSort" in str(response.url):
            listData = re.findall('cat=(.*?)"', response.body.decode("utf-8"))
            #for eveData in listData[:2]:#先取2个测试一下
            listData=["9987,653,655"]#只取手机这个类目
            for eveData in listData:#先取2个测试一下
                if "&" in eveData:
                    eveData = eveData.split("&")[0]
                yield scrapy.Request(url="https://list.jd.com/list.html?cat=%s" % (eveData),callback=self.getGoodsUrl, dont_filter=True)
                yield scrapy.Request(url="https://list.jd.com/list.html?cat=%s&page=2&" % (eveData), callback=self.getGoodsUrl, dont_filter=True)



    def getGoodsUrl(self, response):
        # url Demo: https://list.jd.com/list.html?cat=9987,653,655&page=3

        try:
            pageNum = re.findall("page=(.*?)&", response.url)[0]#1，2，3，311只取第一个就是1

            try:
                totalNum = response.xpath('//span[@class="p-skip"]/em/b/text()').extract()[0]
                #totalNum = 10#取为10测试一下
            except:
                totalNum = 1

            if int(totalNum) > int(pageNum):
                newPageNum = int(pageNum) + 1
                newUrl = str(response.url).replace("page=%s" % (pageNum), "page=%d" % (newPageNum))
                yield scrapy.Request(url=newUrl, callback=self.getGoodsUrl, dont_filter=True)
        except:
            pass

        pageSource = response.body.decode("utf-8")
        if pageSource:
            #for eveId in re.findall("item.jd.com/(.*?).html", pageSource)[:10]:#取为10测试一下
            for eveId in re.findall("item.jd.com/(.*?).html", pageSource):#取为10测试一下#8735304
                urlData = "https://sclub.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=5&page=1&pageSize=10" % (eveId)
                yield scrapy.Request(url=urlData, callback=self.getCommentsData, dont_filter=True)
        else:
            print(response.body.decode("utf-8"))
            print("--------------地址出错，已经记录到本地文件--------------")
            with open("error.txt", "a") as f:
                f.write(response.url + "\n")



    def getCommentsData(self, response):
        # url Demo: https://sclub.jd.com/comment/productPageComments.action?productId=6683017&score=0&sortType=5&page=2&pageSize=10

        pageNum = re.findall("page=(.*?)&",response.url)[0]
        try:
            jsonData = json.loads(response.body.decode("gbk"))
            totalNum = jsonData["productCommentSummary"]["commentCount"]

            for eveComment in jsonData["comments"]:
                item = JdspiderItem()
                item['uid']=eveComment["id"]
                item['creationTime']=eveComment["creationTime"]
                item['firstCategory']=eveComment["firstCategory"]
                item['secondCategory']=eveComment["secondCategory"]
                item['thirdCategory']=eveComment["thirdCategory"]
                item['productId']=eveComment["referenceId"]
                item['content']=eveComment["content"]
                item['score']=eveComment["score"]
                print(item['content'])
                
                yield item

            if int(totalNum) / 10 > int(pageNum):
                newPageNum = int(pageNum) + 1
                newUrl = str(response.url).replace("page=%s" % (pageNum), "page=%d" % (newPageNum))
                yield scrapy.Request(url=newUrl, callback=self.getCommentsData, dont_filter=True)
        except Exception as e:
            print(response.body.decode("gbk"))
            print("************地址出错，已经记录到本地文件***************")
            with open("error.txt","a") as f:
                f.write(response.url + "\n")
