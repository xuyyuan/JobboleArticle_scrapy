# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb  # 注意‘MySQLdb’里面的‘y’, 'db'要小写
from twisted.enterprise import adbapi
import MySQLdb.cursors


class JobboleArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagesPipeline(object):
    pass


class MysqlPipeline(object):
    def __init__(self):
        self.connect = MySQLdb.connect(host='localhost', user='root', password='123456', port=3306,
                                       db='jobbole_article', charset='utf8', use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, url, create_date, tags, praise_nums, fav_nums, comment_nums, front_image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (
        item['title'], item['url'], item['create_date'], item['tags'], item['praise_nums'], item['fav_nums'],item['comment_nums'], item['front_image_url']))
        self.connect.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset = 'utf8',
            use_unicode = True,
            cursorclass = MySQLdb.cursors.DictCursor,  # 这里要注意要引入 import MYSQL_db.cursors
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider): # 其实有时间应该看看twisted的异步框架
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item) # item是要插入的数据
        query.addErrback(self.handle_error, item, spider) # 处理异常；这里的item和spider参数可以不传

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)  # 不要误写成"failure"字符串哦

    def do_insert(self, cursor, item):   # 注意cursor参数哦
        # 执行具体的插入
        insert_sql = """
                   insert into article(title, url, create_date, tags, praise_nums, fav_nums, comment_nums, front_image_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               """
        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['tags'], item['praise_nums'], item['fav_nums'],item['comment_nums'], item['front_image_url']))



