# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo

class JdspiderPipeline(object):

    collection = 'comment_detail'

    # 定义集合名，也就是表的名字，不是库名，库名是mongo_db，也就是Settings文件找中定义的MONGO_DB
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ###
        # scrapy框架提供的一个方法，用于访问settings里的变量或属性，
        # 一般写入MongoDB需要从settings文件中，获得数据库的uri和数据库名称
        ###
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        ###
        # scrapy框架提供的一个方法，爬虫一旦开启，就会实现这个方法，用于连接到数据库
        ###
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ###
        # scrapy框架提供的一个方法，爬虫一旦关闭，就会实现这个方法，用于关闭数据库
        ###
        self.client.close()

    def process_item(self, item, spider):
        ###
        # scrapy框架提供的一个方法，用于处理爬虫的数据，以及怎么保存到MongoDB
        ###
        if not item['content']:
            return item

        data = {
            'uid': item['uid'],
            'creationTime': item['creationTime'],
            'firstCategory': item['firstCategory'],
            'secondCategory': item['secondCategory'],
            'thirdCategory': item['thirdCategory'],
            'productId': item['productId'],
            'content': item['content'],
            'score': item['score']
        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item
        
class DuplicatesPipeline(object):
    #item去重
    def __init__(self):
        self.item_uid_creationTime = set()

    def process_item(self, item, spider):
        uid = item['uid']
        creationTime = item['creationTime']
        uid_creationTime=str(uid)+str(creationTime)
        if uid_creationTime in self.item_uid_creationTime:
            raise DropItem("Duplicate item_uid_creationTime found:%s" % item)

        self.item_uid_creationTime.add(uid_creationTime)
        return item