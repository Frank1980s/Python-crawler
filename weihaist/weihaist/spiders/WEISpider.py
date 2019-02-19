#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Frank
# @Date  : 2019/2/13 11:35

# @File  : WEISpider.py

import scrapy
import copy
from weihaist.items import WeihaistItem
from weihaist.DBUtils import DBUtil


class WEISpider(scrapy.Spider):
    name = 'WEISpider'
    host = "http://xxx.xxx.xxx"

    def __init__(self, flag='list', **kwargs):
        super().__init__(**kwargs)
        self.flag = flag

    def start_requests(self):
        if self.flag == "list":
            url = self.host + '/apps/project.html'
            for i in range(1,7):
                self.page = i
                data = {
                    'keyWord':'',
                    'pjName':'',
                    'cmName':'',
                    'addDate':'',
                    'industry':'',
                    'status':'0',
                    'currentPage':str(self.page)
                }
                yield scrapy.FormRequest(url = url, formdata = data, callback = self.parse, dont_filter = True, meta = {'data':copy.deepcopy(data)})
        elif self.flag == "content":
            # yield scrapy.Request(url='http://xxx.xxx.xxx/apps/projectInfo.html?id=78',callback=self.parse_content)
            urls = DBUtil().get_all_none_url()
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=False)


    def parse(self, response):
        if response.status != 200:
            data = response.meta['data']
            yield scrapy.FormRequest(url = response.url, formdata = data, callback = self.parse, dont_filter = True, meta = {'data':copy.deepcopy(data)})
        if response.status == 200:
            # 项目列表 xpath找的方式为找class为information_box下面的所有超链接
            lis = response.xpath('//div[@class="information_box"]//div[@class="lefttitle"]//a/@href').extract()
            for li in lis:
                url = self.host + '/apps/' + li
                item = WeihaistItem()
                item['url'] = url
                item['page'] = response.meta['data']['currentPage']
                item['Project_name'] = ''
                item['Update_time'] = ''
                item['Project_status'] = ''
                item['Industry_field'] = ''
                item['Publish_enterprise_name'] = ''
                item['Publish_enterprise_address'] = ''
                item['Registered_capita'] = ''
                item['Contacts'] = ''
                item['Phone'] = ''
                item['Email'] = ''
                item['Summary_of_Project_Content'] = ''
                item['Requirements'] = ''
                item['Ways_of_cooperation'] = ''
                item['time'] = ''

                yield item


    def parse_content(self, response):
        if response.status == 200:
            data = {'url': response.url, 'page':''}

            # 项目名称
            Project_name = response.xpath('//div[@class="information_box"]//div[@class="cm_title"]//text()').extract()
            data['Project_name'] = Project_name

            # 更新时间、项目状态
            adata = response.xpath('//div[@class="information_box"]//div[@class="titleDetail"]//div//text()').extract()
            data['Update_time'] = adata[1]
            data['Project_status'] = adata[4]

            # 项目字段
            xdata = response.xpath('//div[@class="information_box"]//div[@class="cardDetail exdetails"]//text()').extract()

            # 行业领域
            data['Industry_field'] = xdata[5]

            # 发布企业名称
            data['Publish_enterprise_name'] = xdata[8]

            # 发布企业地址
            data['Publish_enterprise_address'] = xdata[11]

            # 注册资金
            data['Registered_capita'] = xdata[14]

            # 联系人
            data['Contacts'] = xdata[17]

            # 手机
            data['Phone'] = xdata[20]

            # 邮箱
            data['Email'] = xdata[23]

            # 项目内容概述
            bdata = response.xpath('//div[@class="information_box"]\
            //div[@class="cardDetail exdetails"]//div[@class="logrow"]').xpath('string(.)').extract()

            # 项目内容概述
            data['Summary_of_Project_Content'] = bdata[4].replace("项目内容概述：", "", 1)

            # 资格要求
            data['Requirements'] = bdata[5].replace("资格要求：", "", 1)

            # 合作方式
            data['Ways_of_cooperation'] = bdata[6].replace("合作方式：", "", 1)

            item = WeihaistItem(data)

            yield item

