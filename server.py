#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import torndb
import MySQLdb
import subprocess

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="Activity", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="password", help="database password")


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class PublishHandler(BaseHandler):
    def get(self):
        title = self.get_query_argument("Title", "unSelected")
        self.render("publish.html", Title=title)

    def post(self):
        actName = self.get_argument("actName")
        Title = self.get_argument("Title")
        actTime = self.get_argument("actTime")
        actLoc = self.get_argument("actLoc")
        actIntru = self.get_argument("actIntru")
        actFor = self.get_argument("actFor")
        actPub = self.get_argument("actPub")
        actJoin = self.get_argument("actJoin")
        actDDL = self.get_argument("actDDL")
        actDetail = self.get_argument("actDetail")
        # optional item is follwing
        PEChapter = self.get_argument("PEChapter", None)
        welTime = self.get_argument("welTime", None)
        other = self.get_argument("other", None)
        actDem = self.get_argument("actDem", None)
        print "Time: "+actTime+" Name: "+actName+" Title: "+Title
        try:
            self.db.execute(
                "INSERT INTO activity (actName,actType,actTime,actLoc,actIntru,actFor,actPub,actJoin,actDDL,actDetail,PEChapter,welTime,other,actDem)"
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                actName,Title,actTime,actLoc,actIntru,actFor,actPub,actJoin,actDDL,actDetail,PEChapter,welTime,other,actDem)
        except MySQLdb.ProgrammingError:
            print "request is not allowed"

        self.redirect("/success-publish")

class SuccessPubHandler(BaseHandler):
    def get(self):
        self.render("publish-success.html")
    
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/publish", PublishHandler),
            (r"/success-publish", SuccessPubHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
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

                

def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
    print "server is starting"
    main()