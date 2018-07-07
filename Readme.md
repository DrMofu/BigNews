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

4. mysql数据库设置

在mysql中输入
```
create database db_bignews
```
在config.py文件中将USERNAME和PASSWORD改为你自己mysql的用户名和密码

5. 数据库创建

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py init_user
```

<!-- 3. 创建数据库
```
python manage.py init_db
```
 -->
## 使用
```
python index.py
```

## 文件说明
- index.py                  主程序
- config.py                 配置文件
- crawler.py                爬虫文件
- decoratores.py            定义装饰器
- exts.py                   定义公用的db，防止循环引用
- manage.py                 存放各类操作指令，如数据库创建
- models.py                  提供ORM方法的对数据库操作
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

2018.6.30
- 更换了数据库，改为sqlite
- 添加部分爬虫文件

2018.7.2
- 换回使用mysql数据库，找到之前出错问题。数据库搭建出ORM中类首字母大写，其余内容均小写

2018.7.3
- 整合系统

2018.7.5
- 整合系统，初步完成
- 点赞功能

todo
分类完善-按分类查询 按分类提交

关注
页面跳转优化