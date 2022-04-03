# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Job51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fieldnames = [
        'job_href',
        'job_name',
        'issue_date',
        'company_name',
        'salary',
        'work_area',
        'company_type',
        'company_size',
        'job_welfare',
        'company_industry',
        'job_exp',
        'job_edu',
    ]
    for field in fieldnames:
        exec('{} = Field()'.format(field))
