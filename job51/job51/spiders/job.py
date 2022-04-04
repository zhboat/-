'''
TODO
'''



import json
import requests
import scrapy
import re
from scrapy import Request
from job51.settings import IPPOOL
from job51.items import Job51Item

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
        # 动态ip  -- 本人是付费购买的ip代理池，请自行更换
        # url = 'IP池api'
        # res = requests.get(url)
        # json_data = res.json()
        # datas = json_data.get('data')
        # for data in datas.get('data'):
        #     ip = 'http://' + data['ip'] + ':' + data['port']
        #     IPPOOL.append(ip)
        api_url = 'IP池api'
        ips = requests.get(api_url)
        for ip in ips.text.split('\r\n'):
            if ip:
                IPPOOL.append('http://' + ip)

        for url in self.start_urls:
            for i in range(1,self.max_page):
                yield Request(url.format(self.keyword,i), dont_filter=True, meta={'page': i})

    def parse(self, response):
        data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', response.text)[0]
        json_data = json.loads(str(data))
        engine_jds = json_data['engine_jds']
        for engine_jd in engine_jds:
            item = Job51Item()
            attribute_text = engine_jd.get('attribute_text')
            job_href = engine_jd.get('job_href')
            # 职位链接
            item['job_href'] = re.split('\?',job_href)[0]
            # 职位名称
            item['job_name'] = engine_jd.get('job_name')
            # 发布日期
            item['issue_date'] = engine_jd.get('issuedate')
            # 公司名称
            item['company_name'] = engine_jd.get('company_name')
            # 薪水
            salary = engine_jd.get('providesalary_text')
            if salary:
                item['salary'] = salary
            else:item['salary'] = '面谈'
            # 工作地点
            item['work_area'] = engine_jd.get('workarea_text')
            # 公司类型
            company_type = engine_jd.get('companytype_text')

            if company_type:
                item['company_type'] = company_type
            else: item['company_type'] = '不详'
            # 公司规模
            company_size = engine_jd.get('companysize_text')
            if company_size:
                item['company_size'] = company_size
            else: item['company_size'] = '未知'
            # 职位福利
            job_welfare =  engine_jd.get('jobwelf')
            if job_welfare:
                item['job_welfare'] = job_welfare
            else: item['job_welfare'] = '无'
            # 所属行业
            company_industry = engine_jd.get('companyind_text')
            if company_industry:
                item['company_industry'] = company_industry
            else:
                item['company_industry'] = '未知'
            # 工作经验
            item['job_exp'] = ''
            # 学历
            item['job_edu'] = ''
            for attr in attribute_text:
                for job_exp in self.job_exp_list:
                    if job_exp in attr:
                        item['job_exp'] = attr.strip()
                for job_edu in self.job_edu_list:
                    if job_edu in attr:
                        item['job_edu'] = attr.strip()
                        pass
                    pass
                pass
            if not item['job_edu']:
                item['job_edu'] = '其他'
            if not item['job_exp']:
                item['job_exp'] = '不详'
            yield item