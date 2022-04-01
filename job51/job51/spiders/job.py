'''
TODO
1. 换页就error？

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
        # 动态ip
        url = 'http://proxy.httpdaili.com/apinew.asp?ddbh=1529963582497768589'
        ips = requests.get(url)
        for ip in ips.text.split('\r\n'):
            IPPOOL.append('http://'+ip)
        for url in self.start_urls:
            for i in range(1,self.max_page):
                yield Request(url.format(self.keyword,i), dont_filter=True, meta={'page': i})

    def parse(self, response):
        data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>',response.text)[0]
        json_data = json.loads(str(data))
        engine_jds = json_data['engine_jds']
        for engine_jd in engine_jds:
            item = Job51Item()
            attribute_text = engine_jd.get('attribute_text')
            job_href = engine_jd.get('job_href')
            # 职位链接
            item['job_href'] = re.split('\?',job_href)[0]
            # 职位id
            item['job_id'] = engine_jd.get('jobid')
            # 职位名称
            item['job_name'] =engine_jd.get('job_name')
            # 发布日期
            item['issue_date'] = engine_jd.get('issuedate')
            # 公司名称
            item['company_name'] = engine_jd.get('company_name')
            # 薪水
            item['salary'] = engine_jd.get('providesalary_text')
            # 工作地点
            item['work_area'] = engine_jd.get('workarea_text')
            # 公司类型
            item['company_type'] = engine_jd.get('companytype_text')
            # 公司规模
            item['company_size'] = engine_jd.get('companysize_text')
            # 职位福利
            item['job_welfare'] = engine_jd.get('jobwelf')
            # 所属行业
            item['company_industry'] = engine_jd.get('companyind_text')
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
            yield item
                #if '招' in attr and '人' in attr:
                #    num = re.findall('招(.*?)人', attr)
                 #   if num:
                 #       item['job_rent'] = num[0]
                 #       if num[0] == '若干':
                 #           item['job_rent'] = '∞'
            #yield Request(job_href, callback=self.parse_details, dont_filter=True, meta={'item': item})

    #def parse_details(self, response):
    #    item = response.meta['item']
    #    jts = response.xpath('//div[@class="tCompany_main"]/div[@class="tBorderTop_box"]')
    #    job_info = ''
    #    job_type = ''
    #    print('\n\n\njts:{}\n\n\n'.format(jts))
    #    try:
    #        for jt in jts:
    #            if jt.xpath('./h2/span/text()').extract_first() == '职位信息':
    #                job_info = '\n'.join([i.strip() for i in jt.xpath('./div//text()').extract() if i.strip() != ''])
    #                print('\n\n\nfor_job_info:{}\n\n'.format(job_info))
    #        job_type = response.xpath('//p[@class="fp"]/a/text()').extract_first()
    #        print('\n\n\nfor_job_type:{}\n\n'.format(job_type))
    #    except IndexError:
    #        pass
    #    print('\n\n\njob_info:{}\n\n'.format(job_info))
    #    print('\n\n\njob_type:{}\n\n'.format(job_type))

    #    data = {
    #        'job_info': job_info,
    #        'job_type': job_type,
    #    }
    #    item.update(data)
