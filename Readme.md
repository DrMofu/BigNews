# Big News 新闻管理网站系统
- 为用户提供实时热点新闻

- 采用**python3**，flask框架，需要下载mysql 

## 环境配置
1. 安装python3，建议新手直接下载使用anaconda

- [anaconda官网](https://www.anaconda.com/download/) 或 [清华镜像](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

2. 安装必要的python包：flask. pymysql, flask_sqlalchemy, flask_script, flask_migrate

- 可以直接使用 **pip install -r requirements.txt** 安装环境

3. 安装mysql 

- [mysql windows版](https://dev.mysql.com/downloads/installer/)

4. 数据库创建

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## 使用
```
python index.py
```

## 文件说明
- index.py                  为主程序
- config.py                 为配置文件
- models.py                 管理数据库数据创建
- index.wsgi                与新浪云服务器有关，忽略即可
- exts.py
- requirements.txt          python包说明
- static                    中存放css，js，img等内容
- templates                 存放html

- test                      为测试文件夹，所有成员可在其中创建一个以自己名称命名的文件夹，并在其中测试各个功能


2018.6.26 
- 创建git库

2018.6.27 
- 构建flask结构
- user用户登录注册模块后台代码

2018.6.28
- 添加bootstrap库文件

2018.6.29
- 添加requirements.txt文件 可以使用如下命令来导入环境
```
pip install -r requirements.txt
```
- 完善数据库