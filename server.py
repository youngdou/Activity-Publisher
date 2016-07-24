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
import base64
import time

from tornado.options import define, options

define("port", default=8001, help="run on the given port", type=int)
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
        QRImageName = self.get_argument("QRImageName");
        print QRImageName+"  QRImageName"
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
    
class ShowCollectionHandler(BaseHandler):
    def get(self):
        actType = self.get_query_argument("Title", None)
        if not actType:
            self.write("请查询相应类型的活动\n")
            return


        activity = self.db.query("SELECT * FROM activity WHERE actType = %s;", actType)
        if not activity:
            self.write("暂时还没有此类型的活动")
            return
        self.render("collection.html", activity=activity)

class ManageHandler(BaseHandler):
    def get(self):
        self.render("manage.html")

class TestImageHandler(BaseHandler):
    def get(self):
        self.render("test.html")

class UploadImageHandler(BaseHandler):
    def post(self):
        base64DataUrlData = self.get_argument("base64Image")
        # 将base64的url_data形式转换为base64data
        base64Data = base64.b64decode((base64DataUrlData.split(","))[1]) 
        fileName = getId()+".png"
        # 获取上层目录
        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))+"/ImageBase"
        # 判断上层目录是否存在ImageBase目录
        isImageBasePathExist = os.path.exists(filePath)
        # 如果不存在就创建
        if not isImageBasePathExist:
            os.mkdir(os.path.join(os.pardir, "ImageBase"))
            print "creat a file(ImageBase) to save image"

        try:
            with open(filePath+"/"+fileName, 'wb') as f:
                f.write(base64Data)
                # post返回的数据
                self.write(fileName)
        except Exception:
            print "IO Error"
            # post返回上传错误的信息
            self.write("UploadError")


def getId():
    timeStr = str(time.time())
    time2form = timeStr.split(".")[0]+"_"+timeStr.split(".")[1]
    return time2form
        


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/publish", PublishHandler),
            (r"/success-publish", SuccessPubHandler),
            (r"/collection", ShowCollectionHandler),
            (r"/manage", ManageHandler),
            (r"/testImage", TestImageHandler),
            (r"/uploadImage", UploadImageHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"ActItem": activityItemModule,
                        "Header": headerModules,
                        "Footer": footerModule},
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

class activityItemModule(tornado.web.UIModule):
    def render(self, activity, index):
        return self.render_string("modules/activityItem.html", activity=activity, index=index)

class footerModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/footer.html")

class headerModules(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/header.html")

def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
    print "server is starting"
    main()
