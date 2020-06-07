
from lib.mysql_session import session
from mysql.models import Proxys


def get_all_proxys():
    return session.query(Proxys).filter().all()


def del_proxy(pid):
    session.query(Proxys).filter_by(id=pid).delete()
    session.commit()
