# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
from weihaist.DBUtils import DBUtil, WEIData

class WeihaistPipeline(object):
    def process_item(self, item, spider):
        # 入库
        data = WEIData()
        data.Project_name = item['Project_name']
        data.Update_time = item['Update_time']
        data.Project_status = item['Project_status']
        data.Industry_field = item['Industry_field']
        data.Publish_enterprise_name = item['Publish_enterprise_name']
        data.Publish_enterprise_address = item['Publish_enterprise_address']
        data.Registered_capita = item['Registered_capita']
        data.Contacts = item['Contacts']
        data.Phone = item['Phone']
        data.Email = item['Email']
        data.Summary_of_Project_Content = item['Summary_of_Project_Content']
        data.Requirements = item['Requirements']
        data.Ways_of_cooperation = item['Ways_of_cooperation']
        data.url = item['url']
        data.page = item['page']
        data.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(data)
        if item['Project_name'] == '':
            DBUtil().insert_weihaist(data)
        else:
            DBUtil().update(data)
