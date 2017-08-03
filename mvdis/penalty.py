# Query traffic penalty record

import io
import json
import requests
from lxml import etree
from PIL import Image


class PenaltyRecord(object):
    QUERY_URL = 'https://www.mvdis.gov.tw/m3-emv-vil/vil/penaltyQueryPayRecord/legal'
    PAGING_URL = ('https://www.mvdis.gov.tw/m3-emv-vil/vil/penaltyQueryPayRecord'
                  '?d-49440-p={page}&method=pagination')
    IMAGE_URL = 'https://www.mvdis.gov.tw/m3-emv-vil/captchaImg.jpg'

    def __init__(self, uid, plate=None):
        self.uid = uid
        self.plate = plate
        self.session = requests.Session()
        self.image = None
        self.data = None
        self.page = 1

        self._init_session()
        self._init_image()

    def _init_session(self):
        self.session.head(self.QUERY_URL)

    def _init_image(self):
        resp = self.session.get(self.IMAGE_URL)
        self.image = Image.open(io.BytesIO(resp.content))

    def _make_data(self, verification_code=''):
        return {
            'stage': 'legal',
            'method': 'queryLegal',
            'uid': self.uid,
            'vilTicket': '',
            'plateNo': self.plate,
            'validateStr': str(verification_code)
        }

    def _get_page(self):
        # Get data
        resp = self.session.get(self.PAGING_URL.format(page=self.page))
        root = etree.HTML(resp.text)
        data = root.xpath('//input[@id="json"]/@value')

        if not data:
            raise ValueError

        self.data = json.loads(data[0])
        return self.data

    def query(self, verification_code):
        resp = self.session.post(self.QUERY_URL,
                    data=self._make_data(verification_code))
        root = etree.HTML(resp.text)
        data = root.xpath('//input[@id="json"]/@value')

        if not data:
            raise ValueError

        self.data = json.loads(data[0])
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
    pe = PenaltyRecord('70373538')
    pe.image.show()
    v = input('>>> ')
    resp = pe.query(v)
    print(pe.goto(100))
