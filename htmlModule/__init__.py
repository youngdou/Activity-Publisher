# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class activityItemModule(tornado.web.UIModule):
    def render(self, activity, index):
        return self.render_string("modules/activityItem.html",
                                    activity=activity,
                                    index=index)

class footerModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/footer.html")

class headerModules(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/header.html")