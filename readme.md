# SciNews
清华大学计算机系2023程序设计训练（python课堂）第一次大作业

作者 : 付甲申

## 项目介绍

本项目首先爬取了来自IT之家、新浪新闻、网易新闻三大新闻网站科技板块的6721条新闻，随后利用这些新闻搭建自己的网站，具有首页、搜索页、列表页、分类页、详情页基本页面。最后分析爬取到的数据，利用可视化得到了三个结论。

## 项目结构
```
SciNews: 项目名
|-- Crawler : 爬虫程序文件夹
|   |-- 163TechListCrawler.py : 网易新闻url爬取
|   |-- ITHomeListCrawler.py : IT之家url爬取
|   |-- SinoTechListCrawler.py : 新浪新闻url爬取
|   |__ htmlCrawler.py : 根据url列表下载相应html文件
|-- Data : html文件存储
|   |-- htmls : html文件存储
|   |   |-- 163 : 网易新闻html
|   |   |-- itHome : IT之家html
|   |   |__ sino : 新浪新闻html
|   |-- 163_urls.txt : 网易新闻url存储
|   |-- itHome_urls.txt : IT之家url存储
|   |__ sino_urls.txt : 新浪新闻url存储
|-- SciNewsSite : Web开发、数据分析
|   |-- .idea : Pycharm项目文件
|   |-- blog : ”blog“ 应用（即”新闻“应用）
|   |   |-- migrations : 数据库迁移管理
|   |   |__ static : 静态文件
|   |   |   |__ blog
|   |   |   |   |-- images : 图片文件
|   |   |   |   |   |-- 163 : 网易新闻图片文件存储
|   |   |   |   |   |-- itHome : IT之家图片文件存储
|   |   |   |   |   |-- sino : 新浪新闻图片文件存储
|   |   |   |   |   |-- delete.png : ”删除“图标
|   |   |   |   |   |-- head.png : 网站logo
|   |   |   |   |   |__ refresh.png : ”刷新“图标
|   |   |   |   |__ xxx.css : 不同网页css文件
|   |   |   |   |-- templates : 模板文件夹
|   |   |   |   |   |__ blog
|   |   |   |   |   |   |__ xxx.html : 不同网页html模板
|   |   |   |   |-- templatetags : 自定义过滤器
|   |   |   |   |-- __init__.py
|   |   |   |   |-- admin.py
|   |   |   |   |-- apps.py
|   |   |   |   |-- models.py : 模型
|   |   |   |   |-- tests.py
|   |   |   |   |-- urls.py : "blog"应用url配置
|   |   |   |   |__ views.py : 视图
|   |-- SciNewsSite : 网站配置
|   |   |-- __init__.py
|   |   |-- asgi.py
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |-- wsgi.py
|   |-- __init__.py
|   |-- 163Parser.py : 网易新闻html解析器
|   |-- itHomeParser.py : IT之家html解析器
|   |-- sinioParser.py : 新浪新闻html解析器
|   |-- db.splite3 : 数据库
|   |-- admin.txt : 管理员账号及密码
|   |-- word_separator.py : 分词器
|   |-- stopwords.txt : 停用词
|   |-- classification.py : 关键词提取与主题分类
|   |-- keywords.csv : 提取到的关键词
|   |-- dataAnalysis.ipynb : 数据分析笔记本
|   |__ manage.py
|--.gitignore
|__ readme.md
```

