#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Frank
# @Date  : 2019/2/14 14:37

# @File  : DBUtils.py

from weihaist.settings import DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD
from sqlalchemy import Column, TEXT, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import colorlog
from colorlog import ColoredFormatter

# log设置
handler = colorlog.StreamHandler()

formatter = ColoredFormatter(
    "%(log_color)s[%(asctime)s] [%(levelname)s]%(reset)s %(message)s",
    datefmt="%H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    }

)

handler.setFormatter(formatter)

logger = colorlog.getLogger("Bot")
logger.addHandler(handler)
logger.level = 10
Base = declarative_base()

# 注解，用来限制类只生成一个实例
def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance

class WEIData(Base):
    __tablename__ = DB_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    Project_name = Column(TEXT)
    Update_time = Column(TEXT)
    Project_status = Column(TEXT)
    Industry_field = Column(TEXT)
    Publish_enterprise_name = Column(TEXT)
    Publish_enterprise_address = Column(TEXT)
    Registered_capita = Column(TEXT)
    Contacts = Column(TEXT)
    Phone = Column(TEXT)
    Email = Column(TEXT)
    Summary_of_Project_Content = Column(TEXT)
    Requirements = Column(TEXT)
    Ways_of_cooperation = Column(TEXT)
    url = Column(TEXT)
    page = Column(TEXT)
    time = Column(TEXT)


@singleton
class DBUtil(object):
    def __init__(self):
        self.engine = None
        self.session = None
        self.init_engine()
        self.urls = [u.url.strip() for u in self.session.query(WEIData).all()]


    def init_engine(self):
        logger.debug('开始连接数据库')
        connect_str = 'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}' \
            .format(username=DB_USERNAME, password=DB_PASSWORD, \
                    host=DB_HOST, port=DB_PORT, dbname=DB_NAME)
        self.engine = create_engine(connect_str, encoding='utf-8', echo=True)
        logger.debug('连接数据库成功')
        logger.debug('开始创建/更新数据库')
        Base.metadata.create_all(self.engine)
        logger.debug('创建/更新数据库成功')
        Session = sessionmaker(bind=self.engine)
        self.session = scoped_session(Session)

    # 判断session是否为空并重连，保持session活性
    def check_env(self):
        if self.session is None or self.engine is None:
            self.init_engine()


    # 插入url及url位置
    def insert_weihaist(self, _weihaist_data):
        self.check_env()
        try:
            if _weihaist_data is not None:
                if _weihaist_data.url.strip() not in self.urls:
                    self.session.add(_weihaist_data)
                    self.session.commit()
                    self.session.flush()
                else:
                    logger.error("插入数据失败，_weihaist_data已存在")
            else:
                logger.error('插入数据失败，_weihaist_data为空')
        except Exception as e:
            logger.error("插入数据失败 %r" % e)


    # 插入url及其位置外其他数据
    def update(self, _weihaist_data):
        self.check_env()
        try:
            self.session.query(WEIData).filter_by(url=_weihaist_data.url).update({
                WEIData.Project_name: _weihaist_data.Project_name,
                WEIData.Update_time: _weihaist_data.Update_time,
                WEIData.Project_status: _weihaist_data.Project_status,
                WEIData.Industry_field: _weihaist_data.Industry_field,
                WEIData.Publish_enterprise_name: _weihaist_data.Publish_enterprise_name,
                WEIData.Publish_enterprise_address: _weihaist_data.Publish_enterprise_address,
                WEIData.Registered_capita: _weihaist_data.Registered_capita,
                WEIData.Contacts: _weihaist_data.Contacts,
                WEIData.Phone: _weihaist_data.Phone,
                WEIData.Email: _weihaist_data.Email,
                WEIData.Summary_of_Project_Content: _weihaist_data.Summary_of_Project_Content,
                WEIData.Requirements: _weihaist_data.Requirements,
                WEIData.Ways_of_cooperation: _weihaist_data.Ways_of_cooperation,
                WEIData.time: _weihaist_data.time,
            })
            self.session.commit()
            self.session.flush()
        except Exception as e:
            logger.error("更新数据库失败 %r" % e)


    # 提取带插入数据的URL：
    def get_all_none_url(self):
        self.check_env()
        try:
            result = self.session.query(WEIData).filter_by(Project_name='').all()
            return [item.url for item in result]
        except Exception as e:
            logger.error("查询失败 %r" % e)
