# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class Brasil247Spider(scrapy.Spider):
    name = 'brasil_247'
    allowed_domains = ['brasil247.com']
    download_delay = 5.0
    start_urls = []
    current_id = 0000

    def __init__(self, *a, **kw):
        super(Brasil247Spider, self).__init__(*a, **kw)
        with open('seeds/brasil_247.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        urls = response.css('h3 a::attr(href)').getall()[2:]
        for url in urls:
            yield response.follow(url, callback=self._br_247_callback)
    
    def _get_author(self, authors):
        self.log(authors)
        if "-" in authors:
            return authors.split("-")[0]
        elif "," in authors:
            return authors.split(",")[0]
        else:
            return authors

    def _br_247_callback(self, response):
        output = RiLab01Item()

        output['_id'] = self.current_id
        output['title'] = response.css('h1::text').get().replace('\n', '')
        output['sub_title'] = response.xpath(
            '//p[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]/text()'
        ).get().replace('\n', '')
        output['author'] = self._get_author(
            response.css('section p strong::text, strong a::text').get()
        )
        output['date'] = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "meta", " " ))]/text()'
        ).get()
        output['section'] = response.url.split('/')[5]
        output['text'] = response.css(
            '.entry p::text, p span::text, p a::text, entry span::text, strong::text'
        ).getall().replace('\n', '')
        output['url'] = response.url
        self.current_id += 1

        yield output

