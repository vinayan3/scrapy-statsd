# -*- coding: utf-8 -*-
import scrapy
from scrapy_statsd.tests.test_project.test_project.items import TestProjectItem

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["github.com"]
    start_urls = (
        'https://github.com/scrapy/scrapy',
    )

    def parse(self, response):
        yield TestProjectItem()