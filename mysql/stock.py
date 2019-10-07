
from lib.mysql_session import session
from mysql.models import Test, PreAnalysisStocks
from lib.decorators import model_to_list, model_to_dict


def get_content():
    res = session.query(Test).all()[0]
    return res.content


@model_to_list
def get_all():
    return session.query(Test).all()


@model_to_dict
def get_one():
    return session.query(Test).all()[0]


def multi_add(name, obj_list):
    session.execute(
        name.__table__.replace(),
        obj_list
    )
    return session.commit()


def update_pre_data():
    session.query(PreAnalysisStocks).update(status=0)
    session.commit()


def del_pre_data():
    session.query(PreAnalysisStocks).filter_by(status=0).delete()
    session.commit()
