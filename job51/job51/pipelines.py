# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem


class Job51Pipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self):
        super().__init__()
        #   # 创建一个mongo数据库连接
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['recruitment']
        self.mycol = db['job']

    def process_item(self, item, spider):
        if any(dict(item).values()):
            # 数据保存到pymongo
            url = {'job_href': item['job_href']}
            update = {'$set': dict(item)}
            self.mycol.update_many(url, update, True)
            return item
        else:
            raise  DropItem()
