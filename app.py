# coding:utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import sys
import torndb
import MySQLdb


reload(sys)
sys.setdefaultencoding('utf8') 
from tornado.options import define, options

# custom modules

from Handlers import *
from htmlModule import *



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/publish", PublishHandler),
            (r"/success-publish", SuccessPubHandler),
            (r"/collection", ShowCollectionHandler),
            (r"/manage", ManageHandler),
            (r"/testImage", TestImageHandler),
            (r"/uploadImage", UploadImageHandler),
            (r"/ImageBase/(\d*_\d*\.png)", ResposeImageHandeler),
            (r"/checkActName", CheckActNameHandler),
            (r"/manage/login", LoginHandler),
            (r"/manage/logout", LogoutHandler),
            # 捕获错误路径
            (r"/(.*)", Error_PageHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"ActItem": activityItemModule,
                        "Header": headerModules,
                        "Footer": footerModule},
            login_url="/manage/login",
            debug=True,
            cookie_secret="2jIuGE32TVmSeZe9a4yep9elQB7NWk5Pmyvn0VKfHPk="
        )
        super(Application, self).__init__(handlers, **settings)

        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

        self.maybe_create_tables()

    def maybe_create_tables(self):
        try:
            self.db.get("SELECT COUNT(*) from activity;")
        except MySQLdb.ProgrammingError:
            subprocess.check_call(['mysql',
                                   '--host=' + options.mysql_host,
                                   '--database=' + options.mysql_database,
                                   '--user=' + options.mysql_user,
                                   '--password=' + options.mysql_password],
                                  stdin=open('schema.sql'))
        finally:
            print "finish start the database"