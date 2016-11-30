
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

 # local
db_host = 'localhost'
db_user = 'root'
db_pass= ''
db_name = 'test'

class SaveItem(object):

    def process_item(self, item, spider):
        db = MySQLdb.connect(db_host, db_user, db_pass, db_name, use_unicode = True, charset = "utf8")
        cursor = db.cursor()
        query = (
            """ INSERT INTO test
               (site_type, rank, title, request_url, response_url, doctype, css,
                js, layout, sidebar, emulate, embed_style_cnt, embed_script_cnt, reg_dt)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now()) """
        )
        bind = (
            item['site'].encode('utf-8'),
            item['rank'].encode('utf-8'),
            item['title'].encode('utf-8'),
            item['req_url'].encode('utf-8'),
            item['res_url'].encode('utf-8'),
            item['doctype'].encode('utf-8'),
            item['css'].encode('utf-8'),
            item['js'].encode('utf-8'),
            item['layout'].encode('utf-8'),
            item['sidebar'].encode('utf-8'),
            item['emulate'].encode('utf-8'),
            item['embed_style_cnt'],
            item['embed_script_cnt']
        )
        cursor.execute(query, bind)
        db.commit()

        # Fetch a single row using fetchone() method.
        #data = cursor.fetchone()
        cursor.close()
        db.close()
