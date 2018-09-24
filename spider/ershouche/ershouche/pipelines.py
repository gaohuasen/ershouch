# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class ErshouchePipeline(object):
    def __init__(self):
        self.filename = open("淘车.txt","a",encoding="utf-8")
    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)
        for key,value in json.loads(content,encoding='utf-8').items():
            if value[-1] == '--':
                self.filename.write('Null,')
            else:
                self.filename.write(value[-1].strip()+',')
        self.filename.write('\n')

        return item
    def close_spider(self,spider):
        self.filename.close()
