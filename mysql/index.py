
from lib.mysql_session import session
from mysql.models import Test


def get_content():
    return session.query(Test).all()
