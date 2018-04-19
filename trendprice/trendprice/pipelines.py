# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,time,codecs


class TrendpricePipeline(object):
    def __init__(self):
        try:
            date = time.strftime("%Y-%m-%d", time.localtime())
            # 文件名称格式data+运行日期
            file_dir_name = './output/data-' + date + '.json'
            self.file = codecs.open(file_dir_name, 'w', encoding='utf-8')
            print('已打开爬虫')
        except Exception as es:
            print(es)

    def process_item(self, item, spider):
        try:
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            print('写入成功')
            return item
        except Exception as es:
            print(es)

    def spider_closed(self, spider):
        self.file.close()
