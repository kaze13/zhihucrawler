from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from example.items import QuestionItemLoader


class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://www.zhihu.com/question/25915380']
    rules = (
        Rule(LinkExtractor(allow=(r'question\/\d+$')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # extract question
        el = QuestionItemLoader(response=response)
        el.add_xpath('id', "//div[@class='zg-wrap zu-main question-page']/@data-urltoken")
        el.add_xpath('title', '//div[@id="zh-question-title"]/h2/text()')
        el.add_xpath('content', "//div[@id='zh-question-detail']/div/node()")
        el.add_value('author', 'todo')
        el.add_xpath('tags', '//a[@class="zm-item-tag"]/text()')
        el.add_xpath('comment_count',
                     "//div[@id='zh-question-meta-wrap']/div[@class='zm-meta-panel']/a[@name='addcomment']/text()[last()]")
        el.add_xpath('watch_count', "//div[@class='zh-question-followers-sidebar']/div/a/strong/text()")
        el.add_xpath('related_question', "//ul[@class='zh-question-related-questions']/li/a/@href")
        el.add_xpath('browesed_count', "//div[@class='zu-main-sidebar']/div[last()]/div/div[last()]/strong[1]/text()")
        el.add_xpath('recent_active_time', "//div[@class='zu-main-sidebar']/div[last()]/div/div[1]/span[1]/text()")
        el.add_xpath('related_watch_count',
                     "//div[@class='zu-main-sidebar']/div[last()]/div/div[last()]/strong[2]/text()")
        el.add_value('url', response.url)
        yield el.load_item()

        # extract answer
