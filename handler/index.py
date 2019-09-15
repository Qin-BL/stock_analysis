
from handler import BaseHandler
from control.index import get_index_content, get_all_content, get_one_content


class IndexHandler(BaseHandler):

    def get(self, op):
        if op == 'index':
            res = get_index_content()
            self.send_json(res)
        if op == 'all':
            self.send_json(get_all_content())
        if op == 'one':
            self.send_json(get_one_content())
