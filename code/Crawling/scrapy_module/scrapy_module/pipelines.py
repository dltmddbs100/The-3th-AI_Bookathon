# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

stopwords = ['책','장원', '공지', '생활글', '월장원', '주장원', '이야기글', '알려드립니다', '필독', '[공지]', '작품','소개', '글틴', '읽어보세요', '발표','리뷰','게시판']

class ScrapyModulePipeline:
    def process_item(self, item, spider):
      if any(ext in item['title'] for ext in stopwords):
        raise DropItem('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
      else:
        return item
