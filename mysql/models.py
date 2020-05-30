
from sqlalchemy import Column, Integer, String, DateTime, Boolean, TIMESTAMP, func, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME
from lib.mysql_session import engine


class BaseModel(object):

    # 告诉sqlalchemy是基类
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }


Base = declarative_base(cls=BaseModel)


class Test(Base):

    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    content = Column(VARCHAR(128), nullable=True, default='hello world')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="update time")


class PreAnalysisStocks(Base):

    """待分析股票表"""

    __tablename__ = 'pre_analysis_stocks'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    code = Column(VARCHAR(128), comment='股票代码')
    name = Column(VARCHAR(128), nullable=False, comment='股票名称')
    detials = Column(VARCHAR(512), nullable=False, comment='变动摘要')
    extent = Column(VARCHAR(128), nullable=False, comment='变化幅度')
    status = Column(Integer, default=1, comment='0是分析过的， 1是新加的 ，添加之前先把之前的设置为0，然后添加，添加后删除掉0的数据')
    notice_time = Column(VARCHAR(128), nullable=False, comment='公告时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="加入时间")


class AnalysisedStocks(Base):

    """分析后结果表"""

    __tablename__ = 'analysised_stocks'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    code = Column(VARCHAR(128), comment='股票代码')
    name = Column(VARCHAR(128), nullable=False, comment='股票名称')
    detials = Column(VARCHAR(512), nullable=False, comment='变动摘要')
    extent = Column(VARCHAR(128), nullable=False, comment='变化幅度')
    mark = Column(Integer, nullable=False, index=True, comment='变化幅度')
    notice_time = Column(VARCHAR(128), nullable=False, comment='公告时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="加入时间")


class User(Base):

    """用户"""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    email = Column(VARCHAR(128), nullable=False, comment='邮箱')
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    times = Column(Integer, nullable=False, default=0, comment="购买的权益次数")


# 创建表
Base.metadata.create_all(engine)


