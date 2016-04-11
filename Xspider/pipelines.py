# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from redlock import Redlock
from redlock import MultipleRedlockException


class XspiderPipeline(object):
    host = '42.96.132.158'
    psd = 'wjdh84928399'

    def __init__(self):
        self.dlm = Redlock([{"host": "42.96.132.158", "port": 6379, "db": 0, 'password': "wjdh84928399"}, ])

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.dlm.servers[0].lpush('urls', item['url'])
        return item

    def close_spider(self, spider):
        pass
