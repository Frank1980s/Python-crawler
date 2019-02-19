# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FsoaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Project_name = scrapy.Field()
    Project_number = scrapy.Field()
    Site_of_implementation = scrapy.Field()
    Update_time = scrapy.Field()
    Project_classification = scrapy.Field()
    Popularity_index = scrapy.Field()
    Closing_date = scrapy.Field()
    Place_of_delivery = scrapy.Field()
    Project_annex = scrapy.Field()
    Project_budget = scrapy.Field()
    Contact_unit = scrapy.Field()
    Contacts = scrapy.Field()
    Contact_number = scrapy.Field()
    Keyword = scrapy.Field()
    Project_brief_introduction = scrapy.Field()
    Contractor_Requirements = scrapy.Field()
    Project_log = scrapy.Field()
    Member_reviews = scrapy.Field()
    url = scrapy.Field()
    list_url = scrapy.Field()
    time = scrapy.Field()

