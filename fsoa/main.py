#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Frank
# @Date  : 2019/2/11 9:29

# @File  : main.py

from scrapy import cmdline

def main():
    cmd = "scrapy crawl FSOASpider -L INFO -a flag=content"
    cmdline.execute(cmd.split())

if  __name__ == '__main__':
    main()