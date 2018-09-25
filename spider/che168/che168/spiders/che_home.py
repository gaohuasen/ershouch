# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from che168.items import Che168Item
from selenium import webdriver

class CheHomeSpider(scrapy.Spider):
    name = 'che_home'
    allowed_domains = ['che168.com']
    start_urls = ['https://www.che168.com/china/list/']
    

    def parse(self,response):
        url_base = 'https://www.che168.com'
#       url_next_page = url_base + response.xpath('//div[@id="listpagination"]/a/@href').extract()[0]
        pattern1 = re.compile(r'href="(/china/a0_0msdgscncgpi1ltocsp\d+?exx0/)"')
        for url in pattern1.findall(response.text):
            url_next_page = url_base + url
            yield scrapy.Request(url_next_page,callback=self.parse)
        
#       url_product = url_base + response.xpath('//div[@class="content fn-clear card-wrap"]/div/div/ul/li/a/@href').extract()[0]
        pattern2 = re.compile(r'href="(/dealer/[\s\S]+?)"')
        for url in pattern2.findall(response.text):
            url_product = url_base + url
            pattern3 = re.compile('\/(\d+?)\.html')
            base = 'https://www.che168.com/CarConfig/CarConfig.html?infoid='
            url_detail = base + pattern3.findall(url_product)[0]
            # yield scrapy.Request(url_product,callback=self.parse_product)
            yield scrapy.Request(url_detail,callback=self.parse)
        pattern3 = re.compile(r'id="CarSpecid" value="(\d+?)"')
        for url in pattern3.findall(response.text)[0]:
            url_info = 'https://cacheapi.che168.com/CarProduct/GetParam.ashx?specid=%d&_callback=configTitle'%int(url)
            yield scrapy.Request(url_detail,callback=self.parse_detail)
        
        
        

#     def parse_product(self, response):
#         item = Che168Item()

#         url_base = 'https://www.che168.com/'

#         item['car_license_time'] = response.xpath('//div[@class="details"]/ul/li[2]/span/text()').extract()   #上牌时间
#         print("上牌时间：",item['car_license_time'])
#         try:
#             now = datetime.now() - datetime.strptime(item['car_license_time'][0],'%Y-%m')
#             item['car_age'] = str(round(now.days/365,2))
#         except Exception as e:
#             item['car_age'] = '--'
#         item['car_brand'] =  response.xpath('//div[contains(@class,"breadnav")]/a[4]/text()').extract() #车型
#         item['car_version'] = response.xpath('//div[contains(@class,"breadnav")]/a[5]/text()').extract()  #车系
#         item['car_price'] = response.xpath('//div[@class="car-price"]/ins/text()').extract()
#         item['car_kind'] = response.xpath('//div[@id="anchor02"]/ul/li[3]/text()').extract()   #微型车，小型车，SUV等等
#         item['car_mileage'] = response.xpath('//div[@class="details"]/ul/li[1]/span/text()').extract()   #表显里程
#         item['car_displacement'] = response.xpath('//div[@class="details"]/ul/li[3]/span/text()').extract()    #汽车排量
#         item['car_gear_box'] = response.xpath('//div[@id="anchor02"]/ul/li[2]/text()').extract()    #变速箱，手动，自动
#         item['car_drive_style'] = response.xpath('//div[@id="anchor02"]/ul/li[6]/text()').extract()    #驱动方式
#         item['car_address'] = response.xpath('//div[@class="details"]/ul/li[4]/span/text()').extract()
#         print(item['car_address'])
# #        url_detail = url_base + response.xpath('//div[@id="anchor02"]/div/a/@href').extract()[0]
# #        print(url_detail)

#         yield item

    def parse_detail(self,response):
        item = Che168Item()
        item['car_brand'] = content['result']['paramtypeitems'][0]['paramitems'][2]['value']
        item['car_version'] = content['result']['paramtypeitems'][0]['paramitems'][0]['value']
        item['car_price'] = response.xpath('//div[@class="present-price"]/text()').extract()
        item['car_origin_price'] = content['result']['paramtypeitems'][0]['paramitems'][2]['value']
        item['car_kind'] = content['result']['paramtypeitems'][0]['paramitems'][3]['value']
        item['car_body'] = content['result']['paramtypeitems'][0]['paramitems'][13]['value']     #后备箱容积
        item['car_trunk'] = content['result']['paramtypeitems'][1]['paramitems'][11]['value']
        item['car_license_time'] = response.xpath('//div[@class="source-info-con"]/p/text()').extract()
        try:
            now = datetime.now() - datetime.strptime(item['car_license_time'][0],'%Y-%m')
            item['car_age'] = str(round(now.days/365,2))
        except Exception as e:
            item['car_age'] = '--'
        item['car_mileage'] = response.xpath('//div[@class="source-info-con"]/p/text()').extract()
        item['car_displacement'] = content['result']['paramtypeitems'][2]['paramitems'][2]['value']
        item['car_fuel_consumption'] = content['result']['paramtypeitems'][0]['paramitems'][-2]['value']
        item['car_gear_box'] = content['result']['paramtypeitems'][0]['paramitems'][11]['value']
        item['car_drive_style'] = content['result']['paramtypeitems'][4]['paramitems'][1]['value']
        item['car_seat'] = content['result']['paramtypeitems'][1]['paramitems'][9]['value']   #座位
        item['car_size'] =  content['result']['paramtypeitems'][1]['paramitems'][-9]['value']   #长宽高
             #油耗
        item['car_address'] = response.xpath('//div[@class="source-info-con"]/p/text()').extract()

        yield item