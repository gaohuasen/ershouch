# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ershouche.items import ErshoucheItem

class TaocheSpider(CrawlSpider):
    name = 'taoche'
    allowed_domains = ['taoche.com']
    start_urls = ['http://www.taoche.com/all/?page=1']
    link_list_1 = LinkExtractor(allow="http\:\/\/www\.taoche\.com\/all\/\?page=\d+\#pagetag")
    link_list_2 = LinkExtractor(allow="http\:\/\/www\.taoche\.com\/buycar\/b\-dealer[a-zA-Z0-9]+\.html\?source=\d+")                                   
                                       
    rules = (
        Rule(link_list_1,process_links='deal_links',follow=True),
        Rule(link_list_2,process_links='deal_links',callback='parse_item',follow=True),
    )
    #def parse_item1(self,response):
        #item = ErshoucheItem()
        #yield item
    

    def parse_item(self, response):
        item = ErshoucheItem()
        
#        item['url_single'] = response.xpath('//div[@id="carlist"]/div/ul/li/div/div/a/@href')
#        item['url_page'] = response.xpath('//div[@class="paging-box the-pages"]/div/a/@href')
        
        content1 = response.xpath('//div[contains(@class,"parameter-configure")]/div[1]/ul')
        content2 = response.xpath('//div[contains(@class,"parameter-configure")]/div[2]/ul')
        item['car_brand'] = content1.xpath('./li[1]/span/a[1]/text()').extract()   #车型
        item['car_version'] = content1.xpath('./li[1]/span/a[2]/text()').extract()  #车系
        item['car_price'] = response.xpath('//strong[@class="price-this"]/text()').extract()
        item['car_kind'] = content1.xpath('./li[5]/span/a/text()').extract()   #微型车，小型车，SUV等等
        item['car_body'] = content2.xpath('./li[4]/span/text()').extract()
        item['car_trunk'] = content2.xpath('./li[5]/span/text()').extract()     #后备箱容积
        item['car_age'] = response.xpath('//div[contains(@class,"details-information-list")]/div[1]/div[1]/div[2]/div[1]/text()').extract()
        item['car_mileage'] = response.xpath('//div[@class="summary-attrs"]/dl[2]/dd/text()').extract()   #表显里程
        item['car_displacement'] = content2.xpath('./li[1]/span/a/text()').extract()    #汽车排量
        item['car_fuel_consumption'] = content2.xpath('./li[2]/span/text()').extract()     #油耗
        item['car_gear_box'] = response.xpath('//div[@class="summary-attrs"]/dl[3]/dd/text()').extract()    #变速箱，手动，自动
        item['car_drive_style'] = content1.xpath('./li[4]/span/text()').extract()    #驱动方式
        item['car_seat'] = content2.xpath('./li[4]/span/text()').extract()    #座位
        item['car_size'] = content2.xpath('./li[3]/span/text()').extract()    #长宽高
        item['car_license_time'] = response.xpath('//div[@class="summary-attrs"]/dl[1]/dd/text()').extract()   #上牌时间
        item['car_address'] = content1.xpath('./li[2]/span/a/text()').extract()
        
        yield item
