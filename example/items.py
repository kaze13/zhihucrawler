# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Identity


class QuestionItem(Item):
    id = Field()
    title = Field()
    content = Field()
    author = Field()
    tags = Field()
    comment_count = Field()
    watch_count = Field()
    related_question = Field()
    browesed_count = Field()
    recent_active_time = Field()
    related_watch_count = Field()
    crawled = Field()
    spider = Field()
    url = Field()


class QuestionItemLoader(ItemLoader):
    default_item_class = QuestionItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    id_in = Identity()