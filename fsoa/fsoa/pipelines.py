# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from fsoa.DBUtils import DBUtil, FSOAData
import datetime

class FsoaPipeline(object):
    def process_item(self, item, spider):
        # 入库
        data = FSOAData()
        data.Project_name = item['Project_name']
        data.Project_number = item['Project_number']
        data.Site_of_implementation = item['Site_of_implementation']
        data.Update_time = item['Update_time']
        data.Project_classification = item['Project_classification']
        data.Popularity_index = item['Popularity_index']
        data.Closing_date = item['Closing_date']
        data.Place_of_delivery = item['Place_of_delivery']
        data.Project_annex = item['Project_annex']
        data.Project_budget = item['Project_budget']
        data.Contact_unit = item['Contact_unit']
        data.Contacts = item['Contacts']
        data.Contact_number = item['Contact_number']
        data.Keyword = item['Keyword']
        data.Project_brief_introduction = item['Project_brief_introduction']
        data.Contractor_Requirements = item['Contractor_Requirements']
        data.Project_log = item['Project_log']
        data.Member_reviews = item['Member_reviews']
        data.url = item['url']
        data.list_url = item['list_url']
        data.time =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(data)
        if item['Project_name'] =='':
            DBUtil().insert_fsoa(data)
        else:
            DBUtil().update(data)


