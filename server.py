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
import sys

# custom module
from Handlers import *
from htmlModule import *
from app import *

reload(sys)
sys.setdefaultencoding('utf8') 
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="Activity", help="database name")
define("mysql_user", default="root", help="database user")

# 设置日志
define("mysql_password", default="password", help="database password")
define("log_file_prefix", \
    default=os.path.join(os.path.dirname(__file__), os.pardir, "ActServerLog/logForActServer"))
define("log_rotate_mode", default='time')   # 轮询模式: time or size
define("log_rotate_when", default='D')      # 单位: S / M / H / D / W0 - W6
define("log_rotate_interval", default=1)   # 间隔

def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()



if __name__ == "__main__":
    print "server is starting"
    main()
