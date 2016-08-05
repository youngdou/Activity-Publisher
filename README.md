# Activity-Publisher-for-WeChat

> Author: YoungDou

## 技术架构：

### 前端
- `weui`
- `weui-jquery`, `jquery`

### 后端
- `python/Tornado`
- `MySQL`


---


## **Getting start**
> 部署简单的tornado+mysql服务器

---

## 安装Mysql
```
//这里请记住密码和数据库端口号，如果没有设置，一般默认为3306
```

## 安装tornado和torndb
```
pip install tornado
pip install torndb
```
必要时加sudo

## 安装Mysql-Python数据库驱动

- 出现错误： `fatal error: Python.h: No such file or directory`

- 原因：没有安装python开发包

- 解决:：`apt-get install Python-dev`

## 创建数据库

1. 首先登陆数据库

2. 创建数据库`Activity`和表`activity`(复制目录下的`schema.sql`到数据库执行即可)

3. 修改server.py里面的数据库地址/端口和密码为本地数据库的相关值,可供修改内容如下
```
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="Activity", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="password", help="database password")
```

## 运行服务器

- 命令
```python
python server.py
```
- 问题
1.如果遇到：`socket.error: [Errno 13] Permission denied`
 
 1. 请使用`sudo python server.py`重新执行命令
 2. 或者检查端口号是否被其他应用占用
 
 2.如果遇到：
```
UserWarning: /home/ubuntu/.python-eggs is writable by group/others and vulnerable to attack when used with get_resource_filename. Consider a more secure location (set with .set_extraction_path or the PYTHON_EGG_CACHE environment variable).
warnings.warn(msg, UserWarning)

```
这是.python-eggs缺少权限导致的

1. 进入`/home/ubuntu`

2. 执行`chmod g-wx,o-wx .python-eggs/`即可


>如果完成以上步骤以后，在浏览器/ping/curl访问不了，有可能是云主机的安全组问题---没有开放相关端口，请到云主机管理后台进行设置

---

## 数据维护

另外，在前端上传图片以后，`server.py`会在服务器文件夹上层创建一个`ImageBase`文件夹，用于存放图片`保存为png格式`

所以需要维护的数据有：

1. 数据库信息
2. ImageBase文件夹及它下面的图片文件