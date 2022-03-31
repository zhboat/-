'''
TODO
1. 换页就error？

'''



import json
import pprint
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
        'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
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
        #url = 'https://www.padaili.com/proxyapi?api=t3Zmzk29TLx4dIELsJVzXEJg3eaIN4Cb&num=100&type=1&xiangying=1&order=xiangying'
        url = 'http://proxy.httpdaili.com/apinew.asp?ddbh=1528226256640768589'
        ips = requests.get(url)
        for ip in ips.text.split('\r\n'):
            IPPOOL.append('http://'+ip)
        for url in self.start_urls:
            yield Request(url.format(self.keyword, 1), dont_filter=True, meta={'page': 1})

    def parse(self, response):
        print('\n\n\nheader:{}\n\n\n'.format(response.headers))
        #data = response.text
        print(response.text)
        data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>',response.text)[0]
        json_data = json.loads(str(data))
        page = response.meta['page']
        curr_page = json_data['curr_page']
        total_page = json_data['total_page']
        engine_jds = json_data['engine_jds']
        for engine_jd in engine_jds:
            job_id = engine_jd.get('jobid')  # jobid
            job_name = engine_jd.get('job_name')  # 职位名称
            item = Job51Item()
            item['job_id'] = job_id
            item['keyword'] = self.keyword
            item['job_name'] = job_name
            item['date'] = engine_jd.get('issuedate')  # 发布日期
            item['company_name'] = engine_jd.get('company_name')  # 公司名
            item['salary'] = engine_jd.get('providesalary_text')  # 薪水
            item['workplace'] = engine_jd.get('workarea_text')  # 工作地点
            attribute_text = engine_jd.get('attribute_text')
            item['job_exp'] = ''  # 工作经验
            item['job_edu'] = ''  # 学历
            item['job_rent'] = ''  # 招聘人数
            for attr in attribute_text:
                for job_exp in self.job_exp_list:
                    if job_exp in attr:
                        item['job_exp'] = attr.strip()
                for job_edu in self.job_edu_list:
                    if job_edu in attr:
                        item['job_edu'] = attr.strip()
                if '招' in attr and '人' in attr:
                    num = re.findall('(\d+)', attr)
                    if num:
                        item['job_rent'] = num[0]
            item['company_type'] = engine_jd.get('companytype_text')  # 公司类型
            item['company_size'] = engine_jd.get('companysize_text')  # 公司规模
            item['job_welfare'] = engine_jd.get('jobwelf')  # 职位福利
            item['company_industry'] = engine_jd.get('companyind_text')  # 所属行业
            job_href = engine_jd.get('job_href')
            #yield Request(job_href, callback=self.parse_details, dont_filter=True, meta={'item': item})
        if page < int(total_page) and page < self.max_page:
            page += 1
            #print('\n\n\nself.start_urls:{}\n\n\n'.format(self.start_urls))
            #print('\n\n\nself.start_urls[0]:{}\n\n\n'.format(self.start_urls[0].format(self.keyword, page)))
            #print('\n\n\npage:{}\n\n\n'.format(page))
            #print('\n\n\ntotal_page:{}\n\n\n'.format(total_page))
            #print('\n\n\nmax_page:{}\n\n\n'.format(self.max_page))
            yield Request(self.start_urls[0].format(self.keyword, page), callback=self.parse, dont_filter=True, meta={'page': page},)

    def parse_details(self, response):
        item = response.meta['item']
        jts = response.xpath('//div[@class="tCompany_main"]/div[@class="tBorderTop_box"]')
        job_info = ''
        job_type = ''
        try:
            for jt in jts:
                if jt.xpath('./h2/span/text()').extract_first() == '职位信息':
                    job_info = '\n'.join([i.strip() for i in jt.xpath('./div//text()').extract() if i.strip() != ''])
            job_type = response.xpath('//p[@class="fp"]/a/text()').extract_first()
        except IndexError:
            pass

        data = {
            'job_info': job_info,
            'job_type': job_type,
        }
        item.update(data)
        #yield item
