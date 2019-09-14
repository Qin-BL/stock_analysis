
from lib.redis import rs
from mysql.index import get_content


def get_index_content(id=1):
    res = rs.get('index_content')
    if not res:
        res = get_content()
    return res
