
from lib.mysql_session import session
from mysql.models import Test


def get_content():
    res = session.query(Test).all()[0]
    return res.content