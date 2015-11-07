# -*- coding: utf-8 -*-
import scrapy
from vietnamnet.items import VietnamnetItem


class VietnamnetCrawlSpider(scrapy.Spider):
    name = "vietnamnet_crawl"
    allowed_domains = ["vietnamnet.vn"]
    start_urls = (
        'http://vietnamnet.vn',
    )

    def parse(self, response):
        for top_url in response.xpath('//ul[@class="menu-top clearfix"]/li[@class="item"]/a/@href').extract()[1:]:
            url = response.urljoin(top_url)
            yield scrapy.Request(url, callback=self.parse_top_menu)

    def parse_top_menu(self, response):
        for sel in response.xpath('//div[@class="ArticleCateList"]/div/div'):
            link = sel.xpath("a/@href")
            if link:
                url = response.urljoin(link.extract()[0])
                yield scrapy.Request(url, callback=self.parse_dir_contents)
        
        next_page = response.xpath('//a[@class="ButtonImageText BtnCategoryListNext"]/@href').extract()
        if next_page:
            link = next_page[0]
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_top_menu)
        else:
            return
    
    def parse_dir_contents(self, response):
        item = VietnamnetItem()
        item["title"] = response.xpath('//h1[@class="title"]/text()').extract()
        ori_url = response.xpath("//meta[@property='og:url']/@content").extract()
        if ori_url:
            item["link"] = ori_url[0]
        
        item["content"] = []
        for p_tag in response.xpath('//div[@class="ArticleContent"]/p/text()'):
            item["content"].append(p_tag.extract().strip())
            # print p_tag.extract()
            # output.append(p_tag.extract().strip())
        yield item
