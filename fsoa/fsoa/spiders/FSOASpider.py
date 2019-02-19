#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Frank
# @Date  : 2019/2/11 9:29

# @File  : FSOASpider.py

import scrapy
from fsoa.items import FsoaItem
from fsoa.DBUtils import DBUtil


class FSOASpider(scrapy.Spider):
    name = 'FSOASpider'
    host = "http://xxxx"

    def  __init__(self, flag='list', **kwargs):
        super().__init__(**kwargs)
        self.flag = flag

    def start_requests(self):
        if self.flag =="list":
            for i in range(1,128):
                url = self.host + '/index.php/trade/project_list/0/{page}'.format(page = i)
                yield scrapy.Request(url = url, callback = self.parse, dont_filter = False)
                self.list_url = None

        elif self.flag == "content":
            # yield scrapy.Request(url='http://xxx.xxx.xxx/index.php/trade/project_show/20090',
            #                      callback=self.parse_content)
            urls = DBUtil().get_all_none_url()
            for url in urls:
                yield scrapy.Request(url = url, callback = self.parse_content, dont_filter = False)



    def parse(self, response):
        if response.status != 200:
            yield scrapy.Request(url = response.url, callback = self.parse, dont_filter = True)
        if response.status == 200:
            # 项目列表 xpath找的方式为找class为find-project-layout下面的所有超链接
            lis = response.xpath('//div[@class="find-project-layout"]//div[@class="ti-title w500 fl ofh"]//a/@href').extract()
            for li in lis:
                url = li
                item = FsoaItem()
                item['url'] = url
                item['list_url'] = response.url
                item['Project_name'] = ''
                item['Project_number'] = ''
                item['Site_of_implementation'] = ''
                item['Update_time'] = ''
                item['Project_classification'] = ''
                item['Popularity_index'] = ''
                item['Closing_date'] = ''
                item['Place_of_delivery'] = ''
                item['Project_annex'] = ''
                item['Project_budget'] = ''
                item['Contact_unit'] = ''
                item['Contacts'] = ''
                item['Contact_number'] = ''
                item['Keyword'] = ''
                item['Project_brief_introduction'] = ''
                item['Contractor_Requirements'] = ''
                item['Project_log'] = ''
                item['Member_reviews'] = ''
                item['time'] = ''

                yield item


    def parse_content(self, response):
        if response.status == 200:
            data = {'url': response.url, 'list_url': '', 'Project_log': ''}

            # 项目名称
            Project_name = response.xpath('//div[@class="npd-tt-box"]/div[@class="fl"]/text()').extract()
            data['Project_name'] = Project_name
            # 项目字段
            xdata = response.xpath('//div[@class="npd-cc-box"]//div//span').xpath('string(.)').extract()
            # 项目编号
            data['Project_number'] = xdata[0]
            # 实施地点
            data['Site_of_implementation'] = xdata[1]
            # 更新时间
            data['Update_time'] = xdata[2]
            # 项目分类
            data['Project_classification'] = xdata[3]
            # 人气指数
            data['Popularity_index'] = xdata[4]
            # 截止日期
            data['Closing_date'] = xdata[5]
            # 交付地点
            data['Place_of_delivery'] = xdata[6]
            # 项目附件
            data['Project_annex'] = xdata[8]
            # 项目预算
            data['Project_budget'] = xdata[9]
            # 联系单位
            data['Contact_unit'] = xdata[11]
            # 联系人
            data['Contacts'] = xdata[12]
            # 联系电话
            data['Contact_number'] = xdata[14]
            # 关键字
            Keyword = response.xpath('//div[@class="npd-cc-box"]//li[@class="cb"]//a/text()').extract()
            data['Keyword'] = Keyword
            # 项目简介
            Project_brief_introduction = response.xpath('//div[@class="project-ccbox"]//div[@class="pji-ccobox mt15"]//p').xpath('string(.)').extract()
            data['Project_brief_introduction'] = ''.join(Project_brief_introduction)
            # 接包商要求
            Contractor_Requirements1 = response.xpath('//div[@class="project-ccbox"]//ul[@class="pd-list"]//div[@class="fl"]').xpath('string(.)').extract()
            Contractor_Requirements2 = response.xpath('//div[@class="project-ccbox"]//div[@class="other-ask-for fl"]/b').xpath('string(.)').extract()
            Contractor_Requirements3 = response.xpath('//div[@class="project-ccbox"]//div[@class="fl ml15 other-af-content"]').xpath('string(.)').extract()
            data['Contractor_Requirements'] = ''.join(Contractor_Requirements1).strip() + '\n' + '  '.join(Contractor_Requirements2 + Contractor_Requirements3)
            # 会员评论
            Member_reviews = response.xpath('//div[@class="project-ccbox"]//div[@id="feed_content_div"]').xpath('string(.)').extract()
            for i in Member_reviews:
                data['Member_reviews'] = i.strip()

            item = FsoaItem(data)

            yield item

