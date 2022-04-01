# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import csv

class Job51Pipeline:
    def process_item(self, item, spider):
        return item

#class MongoPipeline:
    #def __init__(self):
     #   # 创建一个mongo数据库连接
     #   self.client = pymongo.MongoClient("mongodb://localhost:27017/")
      #  pass

   # def process_item(self, item, spider):
        # 数据保存到pymongo
        #db = self.client['Job']
        #print('\n\n\nitem:{}\n\n'.format(item))
        #db.chat.update_many(
        #    {'$set': dict(item)}, True)
        #f = open(file='job.csv', mode='a+', encoding='utf-8-sig')
        #write = csv.writer(f)
