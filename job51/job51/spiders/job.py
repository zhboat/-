import pprint
import json
import requests
import scrapy
import re
from scrapy import Request
from job51.settings import IPPOOL

class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['search.51job.com']
    start_urls = [
        'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html'
    ]
    job_edu_list = ['初中及以下', '高中', '中技', '中专', '大专', '本科', '硕士', '博士', '无学历要求']
    job_exp_list = ['在校生/应届生', '经验']

    def __init__(self, max_page=1500, keyword='python'):
        super().__init__()
        self.max_page = max_page
        self.keyword = keyword

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            max_page=crawler.settings.get('MAX_PAGE'),
            keyword=crawler.settings.get('KEYWORD')
        )

    def start_requests(self):
        # 动态ip
        url = 'http://proxy.httpdaili.com/apinew.asp?ddbh=1528226256640768589'
        ips = requests.get(url)
        for ip in ips.text.split('\r\n'):
            IPPOOL.append('http://'+ip)
        for url in self.start_urls:
            yield Request(url.format(self.keyword, 1), dont_filter=True, meta={'page': 1})

    def parse(self, response):
        data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>',response.text)[0]
        json_data = json.loads(str(data))
        pprint.pprint(json_data)
        engine_jds = json_data['engine_jds']
        for index in engine_jds:
            job_href = index['job_href']
            job_name = index['job_name']
            date = index['issuedate']  # 发布日期
            company_name = index['company_name']  # 公司名
            salary = index['providesalary_text']  # 薪水
            workplace = index['workarea_text']  # 工作地点

