# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErshoucheItem(scrapy.Item):

    car_brand = scrapy.Field()    #车型
    car_version = scrapy.Field()  #车系
    car_price = scrapy.Field()
    car_kind = scrapy.Field()    #微型车，小型车，SUV等等
    car_body = scrapy.Field()
    car_trunk = scrapy.Field()    #后备箱容积
    car_age = scrapy.Field()
    car_mileage = scrapy.Field()   #表显里程
    car_displacement = scrapy.Field()    #汽车排量
    car_fuel_consumption = scrapy.Field()    #油耗
    car_gear_box = scrapy.Field()    #变速箱，手动，自动
    car_drive_style = scrapy.Field()    #驱动方式
    car_seat = scrapy.Field()    #座位
    car_size = scrapy.Field()    #长宽高
    car_license_time = scrapy.Field()    #上牌时间
    car_address = scrapy.Field()    #牌照所在地址
#    url_single = scrapy.Field()
#    url_page = scrapy.Field()