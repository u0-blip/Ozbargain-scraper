# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
import redis
import json

class bargin_Pipeline:
    items = []
    def open_spider(self, spider):
        self.rdb = redis.Redis(db=0, port=6379)
        self.rdb.set('get_front_page', '1')
        
    def close_spider(self, spider):
        self.rdb.set('items', json.dumps(self.items))
        self.rdb.set('get_front_page', '0')
        self.rdb.close()

    def process_item(self, item, spider):
        # line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # self.file.write(line)
        self.items.append(item)
        return item