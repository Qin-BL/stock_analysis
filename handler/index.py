
from handler import BaseHandler
from control.index import get_index_content


class IndexHandler(BaseHandler):

    def get(self):
        res = get_index_content()
        self.write(res)
