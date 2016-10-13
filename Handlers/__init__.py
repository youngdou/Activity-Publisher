# coding:utf-8
import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web
import time
import os
import base64

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get_current_user(self):
        return self.get_secure_cookie("username")


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class PublishHandler(BaseHandler):
    def get(self):
        titleMap = {"welfare":u"公益活动", "PE":u"体育活动", "game":u"比赛信息", "lecture":u"讲座信息", "unSelected":u""}
        title = self.get_query_argument("Title", "unSelected")
        MainTitle = titleMap[title]
        self.render("publish.html", Title=title, MainTitle=MainTitle)

    def post(self):
        try:
            QRImageName = self.get_argument("QRImageName");
        except Exception:
            QRImageName = "no_image"
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
                "INSERT INTO activity (actName,actType,actTime,actLoc,actIntru,actFor,actPub,actJoin,actDDL,actDetail,QRImageName,PEChapter,welTime,other,actDem)"
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                actName,Title,actTime,actLoc,actIntru,actFor,actPub,actJoin,actDDL,actDetail,QRImageName,PEChapter,welTime,other,actDem)
        except MySQLdb.ProgrammingError:
            print "request is not allowed"

        self.redirect("/success-publish")

    
class ShowCollectionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        actType = self.get_query_argument("Title", None)
        if not actType:
            self.write("请查询相应类型的活动\n")
            return

        #首先删除过期的信息
        # 现在的时间
        ISOTIMEFORMAT = '%Y-%m-%d %H:%M'
        LocalTime = time.strftime( ISOTIMEFORMAT, time.localtime())
        print LocalTime
        deleted = self.db.execute("DELETE FROM activity WHERE actDDL <= %s", LocalTime)
        # 查找出所需的信息
        activity = self.db.query("SELECT * FROM activity WHERE actType = %s ORDER BY actDDL;", actType)
        if not activity:
            self.write("暂时还没有此类型的活动")
            return
        self.render("collection.html", activity=activity)

class ManageHandler(BaseHandler):
    @tornado.web.authenticated
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
        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))+"/ImageBase"
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
        
class ResposeImageHandeler(BaseHandler):
    def get(self, ImageName):
        print "\n\nhaha\n\n"
        print ImageName
        fileName = ImageName
        # 获取上层目录
        filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))+"/ImageBase"
        # 判断上层目录是否存在ImageBase目录
        isImageBasePathExist = os.path.exists(filePath)
        if not isImageBasePathExist:
            return

        self.set_header("content-Type", "image/png")
        self.set_header ('Content-Disposition', 'attachment; filename='+fileName)
        with open(filePath+"/"+fileName, "rb") as f:
            while True:
                data = f.read(100)
                if not data:
                    break;
                self.write(data)
        self.finish()

class CheckActNameHandler(BaseHandler):
    def post(self):
        actName = self.get_argument("actName")
        print actName
        activity = self.db.query("SELECT * FROM activity WHERE actName = %s;", actName)
        if not activity:
            self.write("no_exist")
        else:
            self.write("exist")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        # 检查是否管理员账号/密码
        username = self.get_argument("username")
        password = self.get_argument("password")
        if username != "sysuact":
            self.write("error_username")
        elif password != "sysuact":
            self.write("error_password")
        else:
            self.set_secure_cookie("username", username)
            self.redirect("/manage")

class SuccessPubHandler(BaseHandler):
    def get(self):
        self.render("publish-success.html")

class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_secure_cookie("username")):
            self.clear_cookie("username")
            self.redirect(r"/manage/login")

class Error_PageHandler(BaseHandler):
    def get(self, rep):
        self.write_error(404)

    def write_error(self, status_code, **keywd):
        # 不管404 500，一致用一个页面
        self.render("error_404.html")
