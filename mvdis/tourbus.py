# Query tour bus data

import json
import requests
from collections import namedtuple
from lxml import etree


class TourBus(object):
    QUERY_URL = 'https://www.mvdis.gov.tw/m3-emv-mk3/tourBus/'
    PAGING_URL = 'https://www.mvdis.gov.tw/m3-emv-mk3/tourBus/query?d-1332667-p={page}'
    TourBusDetail = namedtuple('TourBusDetail', 'id name city area address phone status')

    def __init__(self):
        self.session = requests.Session()
        self.data = None
        self._init_session()

    def _init_session(self):
        self.session.head(self.QUERY_URL)

    def _get_page(self):
        # Get query page data
        resp = self.session.get(self.PAGING_URL.format(page=self.page))
        root = etree.HTML(resp.text)
        data = root.xpath('//input[@value="詳細資料"]/@onclick')

        if not data:
            raise ValueError

        def _make_data(d):
            return json.loads('[%s]' % (d[9:-2].replace(' ', '').replace("'", '"')))

        self.data = [self.TourBusDetail(*_make_data(d)) for d in data]
        return self.data

    def next(self):
        self.page += 1
        return self._get_page()

    def prev(self):
        if self.page - 1 > 0:
            self.page -= 1
        return self._get_page()

    def goto(self, page):
        self.page = int(page)
        return self._get_page()


if __name__ == '__main__':
    t = TourBus()
    print(t.goto(1))
    resp = t.session.get('https://www.mvdis.gov.tw/m3-emv-mk3/tourBus/query?d-444630-p=2')
    print(resp.text)
