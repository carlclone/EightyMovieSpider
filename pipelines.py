# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import  datetime
import MySQLdb
import json
from scrapy.exporters import JsonItemExporter
from  scrapy.pipelines.images import ImagesPipeline

class JsonWithEncodingPipeline(object):
    # 自定义的导出
    def __init__(self):
        try:
            self.file = codecs.open('eightysmovie_export.json','w',encoding="utf-8")
        except Exception as e:
            create_date = datetime.datetime.now().date()
    def process_item(self,item,spider):
        print('dsad')
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

# 容易阻塞   同步的操作
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','root','scrapy',charset="utf8",use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = """
        insert into 80s (name,description,english_name,type,language,area,release_date,movie_length,douban_rank,tv_download_link,cover)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["name"],item["description"],item["english_name"],item["type"],item["language"],item["area"],item["release_date"],item["movie_length"],item["douban_rank"],item["tv_download_link"],item["cover"]))
        self.conn.commit()

# 用twisted的连接池       异步的操作
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

