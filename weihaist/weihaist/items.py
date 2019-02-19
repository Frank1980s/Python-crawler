# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeihaistItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Project_name = scrapy.Field()
    Update_time = scrapy.Field()
    Project_status = scrapy.Field()
    Industry_field = scrapy.Field()
    Publish_enterprise_name = scrapy.Field()
    Publish_enterprise_address = scrapy.Field()
    Registered_capita = scrapy.Field()
    Contacts = scrapy.Field()
    Phone = scrapy.Field()
    Email = scrapy.Field()
    Summary_of_Project_Content = scrapy.Field()
    Requirements = scrapy.Field()
    Ways_of_cooperation = scrapy.Field()
    url = scrapy.Field()
    page = scrapy.Field()
    time = scrapy.Field()
