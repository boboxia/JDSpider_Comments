# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo

class JdspiderPipeline(object):

    collection = 'comment_detail'

    # ���弯������Ҳ���Ǳ�����֣����ǿ�����������mongo_db��Ҳ����Settings�ļ����ж����MONGO_DB
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ###
        # scrapy����ṩ��һ�����������ڷ���settings��ı��������ԣ�
        # һ��д��MongoDB��Ҫ��settings�ļ��У�������ݿ��uri�����ݿ�����
        ###
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        ###
        # scrapy����ṩ��һ������������һ���������ͻ�ʵ������������������ӵ����ݿ�
        ###
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ###
        # scrapy����ṩ��һ������������һ���رգ��ͻ�ʵ��������������ڹر����ݿ�
        ###
        self.client.close()

    def process_item(self, item, spider):
        ###
        # scrapy����ṩ��һ�����������ڴ�����������ݣ��Լ���ô���浽MongoDB
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
    #itemȥ��
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