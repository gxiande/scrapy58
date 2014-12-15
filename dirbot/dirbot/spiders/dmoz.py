# -*- coding: utf-8 -*-
import re
from scrapy import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.spider import Spider
from scrapy.selector import Selector
from dirbot import settings

from dirbot.items import Website

class DmozSpider(Spider):
    name = "dmoz"

    allowed_domains = [settings.DOMAIN]
    start_urls = [
        settings.START_URL
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('(\?q=*)|(\?s=\d+&q=*)', )), callback='parse_item', follow=True),
    )

    def __init__(self):
        self.province = ""
        self.city = ""
        self.all_urls = settings.KEY_URLS


    def parse(self, response):
            sel = Selector(response)
            urls = sel.xpath('//div[@class="pagerNumber"]/a/@href').extract()
            self.province = sel.xpath('//meta[@name="location"]/@content').extract()[0].split(";")[0].split("=")[1]
            self.city = sel.xpath('//meta[@name="location"]/@content').extract()[0].split(";")[1].split("=")[1]
            primurl = settings.START_URL
            urls.insert(0, primurl)
            if len(urls) != 0:
                    #delete next
                    urls.pop(len(urls)-1)
            for url in urls:
                if url != urls[len(urls)-1]:
                    self.all_urls.append(url)
            for url in urls:
                if url == urls[len(urls)-1]:
                    yield Request(url, callback=self.parse3)




    def parse3(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="pagerNumber"]/a/@href').extract()
        urls2 = []
        if len(urls) != 0:
            #delete pre
            urls.pop(0)
            #delete next
            urls.pop(len(urls)-1)
            for url in urls:
                if url != urls[len(urls)-1]:
                    self.all_urls.append(url)
        else:
            self.all_urls.append("true")
            print len(self.all_urls)
            print self.all_urls
            print self.all_urls[len(self.all_urls)-1]
            if self.all_urls[len(self.all_urls)-1] == "true":
                    for url in self.all_urls:
                        if url != "true":
                           yield Request(url, callback=self.parse2)
        for url in urls:
                if url == urls[len(urls)-1]:
                    yield Request(url, callback=self.parse3)
    def parse2(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        # sel = Selector(response)
        # sites = sel.xpath('//ul[@class="directory-url"]/li')
        # items = []
        #
        # for site in sites:
        #     item = Website()
        #     item['name'] = site.xpath('a/text()').extract()
        #     item['url'] = site.xpath('a/@href').extract()
        #     item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
        #     items.append(item)
        sel = Selector(response)
        trs = sel.xpath('//table[@class="tbimg"]/tbody/tr')
        items = []
        for tr in trs:
            item = Website()
            province = self.province
            # province = sel.xpath('//meta[@name="location"]/@content').extract()[0].split(";")[0].split("=")[1]
            item['province'] = province
            city = self.city
            # city = sel.xpath('//meta[@name="location"]/@content').extract()[0].split(";")[1].split("=")[1]
            item['city'] = city
            district = tr.xpath('td[@class="info"]/ul/li[@class="tli2"]/text()').extract()[0].replace(u'\xa0', u' ').split(u" ")[0].split(u"【")[1]
            item['district'] = district
            name = tr.xpath('td[@class="info"]/ul/li[@class="tli1"]/a/text()').extract()[0].strip()
            item['name'] = name.strip()
            address = province+city+district+name
            item['address'] = address
            items.append(item)
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"+str(len(items))
        return items
