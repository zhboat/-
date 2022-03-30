# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
from .settings import IPPOOL, COUNT


class Job51SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class Job51HeadersMiddleware:
#    def process_request(self, request, spider):
#        if request.url.startswith('https://jobs.51job.com/'):
#            request.headers.update(
#                {
#                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#                }
#            )
#        else:
#            request.headers.update(
#                {
#                        'Accept': 'application/json, text/javascript, */*; q=0.01',
#                }
#            )
#            pass
#        pass
#    pass

class Job51DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        # 随机选中一个ip
        ip = random.choice(IPPOOL)
        print('当前ip', ip, '-----', COUNT['count'])
        # 更换request的ip----------这句是重点
        request.meta['proxy'] = ip
        # 如果循环大于某个值,就清理ip池,更换ip的内容
        if COUNT['count'] > 50:
            print('-------------切换ip------------------')
            COUNT['count'] = 0
            IPPOOL.clear()
            ips = requests.get('http://proxy.httpdaili.com/apinew.asp?ddbh=1528226256640768589')
            for ip in ips.text.split('\r\n'):
                IPPOOL.append('http://' + ip)
        # 每次访问,计数器+1
        COUNT['count'] += 1
        return None

    # Called for each request that goes through the downloader
    # middleware.

    # Must either:
    # - return None: continue processing this request
    # - or return a Response object
    # - or return a Request object
    # - or raise IgnoreRequest: process_exception() methods of
    #   installed downloader middleware will be called

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# class MyproxiesSpiderMiddleware(object):
#
#
#     def __init__(self, ip=''):
#         self.ip = ip
#         pass
#
#     def process_request(self, request, spider):
#         api = 'http://proxy.httpdaili.com/apinew.asp?ddbh=1528226256640768589'
#         res = requests.get(url=api)
#         thisip = random.choice(res.text)
#         request.meta["proxy"]="http://" + thisip["ipaddr"]
