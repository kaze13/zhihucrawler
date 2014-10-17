# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from datetime import datetime
from hashlib import md5
from scrapy import log
from twisted.enterprise import adbapi


class ExamplePipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item


class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM website WHERE id = %s
        )""", (item['id'], ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE website
                SET name=%s, description=%s, url=%s, updated=%s
                WHERE guid=%s
            """, (item['name'], item['description'], item['url'], now, guid))
            spider.log("Item updated in db: %s %r" % (item['id'], item))
        else:
            conn.execute("""
                INSERT INTO question (id, title, content, author, tags,
                comment_count, watch_count, related_question, browesed_count, recent_active_time
                related_watch_count, crawled, spider, url)
                VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)
            """, ( item['id'], item['title'], item['content'], item['author'], item['tags'], item['comment_count'],
            item['watch_count'], item['related_question'], item['browesed_count'],item['recent_active_time'], item['related_watch_count'],
            item['crawled'],item['spider'], item['url'],))
            spider.log("Item stored in db: %s %r" % (item['id'], item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()