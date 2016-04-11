# coding:utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule, Spider
from scrapy.contrib.linkextractors import LinkExtractor
from Xspider.items import XspiderItem
from scrapy import log, Request
from redlock import Redlock
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
from time import time

class MasterSpider(CrawlSpider):
    name = 'master_spider'
    start_urls = ["http://r2.qq.com/main.shtml", "http://speed.qq.com/main.shtml", "http://cf.qq.com/main.shtml", "http://ffo.qq.com/main.shtml"]
    allowed_domains = ["r2.qq.com", "speed.qq.com", "cf.qq.com", "ffo.qq.com"]
    rules = (Rule(LinkExtractor(allow=('\.htm', '\.shtml'), ), callback='parse_item', follow=True), )

    def parse_item(self, response):
        item = XspiderItem()
        item['url'] = response.url
        return item


class SlaveSpider(Spider):
    name = 'slave_spider'
    default_retry_count = 3
    default_retry_delay = 1
    def __init__(self):
        self.dlm = Redlock([{"host": "42.96.132.158", "port": 6379, "db": 0, 'password': "wjdh84928399"}, ])
        self.list = []
        self.driver = PhantomJS()

    def start_requests(self):
        self.load_payload()
        while True:
            my_lock = self.dlm.lock('URLSLOCK', 1000)
            while isinstance(my_lock, bool):
                pass
            len = self.dlm.servers[0].llen('urls')
            while len > 0:
                url = self.dlm.servers[0].lpop('urls')
                self.dlm.unlock(my_lock)
                urls = self.get_urls(url=url)
                for u in urls:
                    yield Request(url=u, callback=self.parse)
        log.msg('the slave spider is over!', log.WARNING)

    def parse(self, response):
        log.msg(response.url+' is over', log.INFO)

    def get_urls(self, url):
        for l in self.list:
            temp = url + l
            yield temp

    def load_payload(self):
        f = open('Xspider/payload.txt', 'r')
        for line in f.readlines():
            line = line.strip('\n')
            self.list.append(line)
        f.close()
