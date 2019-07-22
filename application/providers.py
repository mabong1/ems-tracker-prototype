import requests
from lxml import html
import re

from exceptions import HttpRequestError

class Provider:
    url = ""
    data = {}
    headers = {}

    def request(self, parser=None):
        if(not parser):
            parser = self.parse
        r = requests.post(self.url, data=self.data, headers=self.headers)
        if(r.status_code != 200):
            raise HttpRequestError
        return parser(r.content)

    @staticmethod
    def parse(response):
        tree = html.fromstring(r.text)
        return tree

class EMS(Provider):
    url = "https://service.epost.go.kr/trace.RetrieveEmsRigiTraceList.comm"
    data = {
        "POST_CODE": "CP216671579KR",
        "displayHeader" : ""
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,ko;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "38",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "service.epost.go.kr",
        "Origin": "https://service.epost.go.kr",
        "Pragma": "no-cache",
        "Referer": "https://service.epost.go.kr/iservice/usr/trace/usrtrc004k01.jsp",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    def __init__(self, parcel):
        self.data["POST_CODE"] = parcel

    @staticmethod
    def parse(response):
        tree = html.fromstring(response)
        delivery_overview, delivery_status = tuple(tree.xpath('//table'))
        pattern = re.compile('[\n\t\xa0\s]+')
        
        return {
            'overview': [(field,value) for field,value in zip(delivery_overview.xpath('thead//th/text()'), [' '.join(node.itertext()).strip() for node in delivery_overview.xpath('(tbody//td | tbody//th)')])],
            'detail': {
                'head': delivery_status.xpath('tr/th/text()'),
                'rows': [text for tr in delivery_status.xpath('tr')[1:] for text in [[re.sub(pattern, ' ', ' '.join(td.itertext())).strip() for td in tr.xpath('td')]]]
            }
        }