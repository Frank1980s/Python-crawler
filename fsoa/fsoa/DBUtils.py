#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author: Frank
# @Date  : 2019/2/13 9:20

# @File  : DBUtils.py

from fsoa.settings import DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD
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

class FSOAData(Base):
    __tablename__ = DB_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    Project_name = Column(TEXT)
    Project_number = Column(TEXT)
    Site_of_implementation = Column(TEXT)
    Update_time = Column(TEXT)
    Project_classification = Column(TEXT)
    Popularity_index = Column(TEXT)
    Closing_date = Column(TEXT)
    Place_of_delivery = Column(TEXT)
    Project_annex = Column(TEXT)
    Project_budget = Column(TEXT)
    Contact_unit = Column(TEXT)
    Contacts = Column(TEXT)
    Contact_number = Column(TEXT)
    Keyword = Column(TEXT)
    Project_brief_introduction = Column(TEXT)
    Contractor_Requirements = Column(TEXT)
    Project_log = Column(TEXT)
    Member_reviews = Column(TEXT)
    url = Column(TEXT)
    list_url = Column(TEXT)
    time = Column(TEXT)


@singleton
class DBUtil(object):
    def __init__(self):
        self.engine = None
        self.session = None
        self.init_engine()
        self.urls = [u.url.strip() for u in self.session.query(FSOAData).all()]


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
    def insert_fsoa(self, _fsoa_data):
        self.check_env()
        try:
            if _fsoa_data is not None:
                if _fsoa_data.url.strip() not in self.urls:
                    self.session.add(_fsoa_data)
                    self.session.commit()
                    self.session.flush()
                else:
                    logger.error("插入数据失败，_fsoa_data已存在")
            else:
                logger.error('插入数据失败，_fsoa_data为空')
        except Exception as e:
            logger.error("插入数据失败 %r" % e)


    # 插入url及其位置外其他数据
    def update(self, _fsoa_data):
        self.check_env()
        try:
            self.session.query(FSOAData).filter_by(url=_fsoa_data.url).update({
                FSOAData.Project_name: _fsoa_data.Project_name,
                FSOAData.Project_number :  _fsoa_data.Project_number,
                FSOAData.Site_of_implementation : _fsoa_data.Site_of_implementation,
                FSOAData.Update_time : _fsoa_data.Update_time,
                FSOAData.Project_classification : _fsoa_data.Project_classification,
                FSOAData.Popularity_index : _fsoa_data.Popularity_index,
                FSOAData.Closing_date : _fsoa_data.Closing_date,
                FSOAData.Place_of_delivery : _fsoa_data.Place_of_delivery,
                FSOAData.Project_annex : _fsoa_data.Project_annex,
                FSOAData.Project_budget : _fsoa_data.Project_budget,
                FSOAData.Contact_unit : _fsoa_data.Contact_unit,
                FSOAData.Contacts : _fsoa_data.Contacts,
                FSOAData.Contact_number : _fsoa_data.Contact_number,
                FSOAData.Keyword : _fsoa_data.Keyword,
                FSOAData.Project_brief_introduction : _fsoa_data.Project_brief_introduction,
                FSOAData.Contractor_Requirements : _fsoa_data.Contractor_Requirements,
                FSOAData.Project_log : _fsoa_data.Project_log,
                FSOAData.Member_reviews : _fsoa_data.Member_reviews,
                FSOAData.time : _fsoa_data.time,
            })
            self.session.commit()
            self.session.flush()
        except Exception as e:
            logger.error("更新数据库失败 %r" % e)


    # 提取带插入数据的URL：
    def get_all_none_url(self):
        self.check_env()
        try:
            result = self.session.query(FSOAData).filter_by(Project_name='').all()
            return [item.url for item in result]
        except Exception as e:
            logger.error("查询失败 %r" % e)