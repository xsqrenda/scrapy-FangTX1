# -*- coding: utf-8 -*-
import scrapy, re
import re
from trendprice.items import PricetrendItem
from urllib.parse import urljoin


class PricetrendSpider(scrapy.Spider):
    name = 'pricetrend'

    # 爬取范围
    # allowed_domains = ["http://esf.gz.fang.com/house-a080/"]
    # 爬取开始页
    start_urls = ["http://esf.lz.fang.com/housing"]
    dataurl = 'http://pinggus.fang.com/RunChartNew/MakeChartData?newcode='
    custom_settings = {
        'ITEM_PIPELINES': {
            'fangprice.pipelines.FangpricePipeline': 1,
        },
        # 'SPIDER_MIDDLEWARES': {
        #     'fangprice.middlewares.FangpriceSpiderMiddleware': 543,
        # },
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'fangprice.middlewares.ChangeUserAgentMiddleware': 80,
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        #     'fangprice.middlewares.ChangeIpProxyMiddleware': 104,
        #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 105
        # }
    }

    def parse(self, response):
        # 初始化item
        item = PricetrendItem()
        # 接收response对象
        resp = scrapy.Selector(response)
        # 提取页面中小区信息列表
        house_list = resp.css(".houseList")[0].css("dl")

        # 得到url
        for i in house_list:
            dt_a = i.css("dt a")
            # 去除空白，源页面中存在
            if len(dt_a) == 1:
                # 提取url
                url = dt_a.xpath("@href")[0].extract()

                # 爬虫进行二级页面信息提取
                req = scrapy.Request(
                    url=url,
                    meta={'item': item},
                    callback=self.parse_second,
                    dont_filter=True
                )
                yield req

        # 页面“下一页”
        next_page = resp.css("a#PageControl1_hlk_next").xpath("@href").extract_first()
        # 最后页面是否还有“下一页”
        if next_page is not None:
            rooturl = self.start_urls[0]
            next_page_url = urljoin(rooturl, next_page)
            # 递归调用自身，实现自动下一页爬取url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )

    # 爬取详细信息的方法
    def parse_second(self, response):
        # 使用同一个item
        item = response.meta['item']
        # 读取详细信息
        chart_url = response.css('#fangjiazs > div.laybox > iframe').xpath("@src")[0].extract()
        item['city'] = chart_url.split('=')[1].split('&')[0]
        item['district'] = chart_url.split('=')[2].split('&')[0]
        item['name'] = chart_url.split('=')[4].split('&')[0]
        # item['name'] = response. \
        #     xpath('//*[@id="body"]/div[6]/div[2]/div[1]/h1/strong/text()')[0].extract()
        # newcode = re.findall("\d+",chart_url)[0]
        item['newcode'] = chart_url.split('=')[3].split('&')[0]
        muburl = self.dataurl + item['newcode']
        item['url'] = muburl
        req = scrapy.Request(
            url=muburl,
            meta={'item': item},
            callback=self.parse_third,
            dont_filter=True
        )
        yield req

    def parse_third(self, response):
        item = response.meta['item']
        item['data'] = response.body.decode('gbk')
        print(item)
        # 保存item
        yield item
