import os
import sys
import django
import re
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SciNewsSite.settings")
django.setup()

from blog.models import Blog, Image
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'}

# 类别变量
STOCK = 1  # 财经板块，不知道为什么会在新浪科技里，可能因为主体是科技公司
CSJ = 2  # 创客记
APPLE = 3  # APPLE

'''
新浪新闻解码器
作者：付甲申
'''


def get_title(soup, category):
    """
    根据不同类别，返回标题
    :param soup: BeautifulSoup对象
    :param category:子类别
    :return: 新闻标题
    """
    if category == STOCK:
        return soup.find("h1", class_="main-title").text
    elif category == CSJ or APPLE:
        return soup.find("h1", id="artibodyTitle").text


def get_time(soup, category):
    """
        根据不同类别，返回发布时间
        :param soup: BeautifulSoup对象
        :param category:子类别
        :return: 新闻发布时间
    """
    if category == STOCK:
        father_div = soup.find("div", class_="date-source")  # 获取父节点
        return datetime.strptime(father_div.find("span", class_="date").text,
                                 "%Y年%m月%d日 %H:%M")  # 转化为datetime格式
    elif category == CSJ:
        return datetime.strptime(re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
                                            soup.find("span", id="pub_date").text)[0],
                                 "%Y-%m-%d %H:%M:%S")  # 转化为datetime格式
    elif category == APPLE:
        return datetime.strptime(re.findall("\d{4}年\d{2}月\d{2}日\d{2}:\d{2}",
                                            soup.find("span", id="pub_date").text)[0],
                                 "%Y年%m月%d日%H:%M")  # 转化为datetime格式


def get_author(soup, category):
    """
        根据不同类别，返回作者
        :param soup: BeautifulSoup对象
        :param category:子类别
        :return: 作者
    """

    if category == STOCK:
        father_div = soup.find("div", class_="date-source")  # 获取父节点
        if father_div.find("span", class_="source") is not None:
            return father_div.find("span", class_="source").text  # 获取author
        return father_div.find(class_="source ent-source").text  # 获取author
    elif category == CSJ:
        return soup.find("span", class_="author", id="author_ename").a.text  # 获取author
    elif category == APPLE:
        return soup.find("span", id="media_name").text  # 获取author


def get_content(soup, category):
    """
        根据不同类别，返回正文
        :param soup: BeautifulSoup对象
        :param category:子类别
        :return: 正文
    """
    if category == STOCK:
        body_texts = [str(p.text).replace("\n", "").replace(" ", "") for p in
                      soup.find("div", class_="article", id="artibody").find_all("p") if
                      p.text is not None]  # 获取列表形式的正文
        body_text = ""
        for text in body_texts:
            body_text += text + "\n"
        return body_text  # 转化为单字符串
    elif category == CSJ or APPLE:
        body_texts = [str(p.text).replace("\n", "").replace(" ", "") for p in
                      soup.find("div", id="artibody").find_all("p") if
                      p.text is not None]  # 获取列表形式的正文
        body_text = ""
        for text in body_texts:
            body_text += text + "\n"
        return body_text  # 转化为单字符串


def get_img_urls(soup, category):
    """
        根据不同类别，返回图片url
        :param soup: BeautifulSoup对象
        :param category:子类别
        :return: 正文
    """
    urls = []
    if category == STOCK:
        urls.extend([img['src'] for img in
                     soup.find("div", class_="article", id="artibody").find_all("img")
                     if img['src'] is not None])  # url列表
    elif category == CSJ or APPLE:
        urls.extend([img['src'] for img in
                     soup.find("div", id="artibody").find_all("img")
                     if img['src'] is not None])  # url列表
    # 据考证，有的链接长得比较奇怪，需要处理一下
    for i in range(len(urls)):
        if not urls[i].startswith("http"):
            urls[i] = "https:" + urls[i]
    return urls


# 获取所有html文件名
fs = []
for root, dirs, files in os.walk("../data/htmls/sino"):
    for file in files:
        fs.append(str(re.findall("(.*)\.html", file)[0]))

print(f"start loading {len(fs)} files")

# 逐文件解析
for file_name in fs:

    with open(f"../data/htmls/sino/{file_name}.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

        # Parse url
        url = soup.find("meta", property="og:url")["content"]

        # 避免重复
        try:
            Blog.objects.get(url=str(url))
        except Blog.DoesNotExist:  # 这里使用try-except块，是因为url不存在时会抛出Blog.DoesNotExist异常，利用这个异常可以避免重复添加
            # 分析网页源码时发现，新浪新闻不同子主题使用的模板并不相同，因此需要分类判断
            # 判断新浪新闻子主题
            category = STOCK
            if soup.find("div", class_="top_logo") is not None:
                category = APPLE
            elif soup.find("h1", id="artibodyTitle") is not None:
                category = CSJ

            # Parse title
            title = get_title(soup, category)
            website = "新浪新闻"

            # Parse time and author
            author_id = get_author(soup, category)
            create_time = get_time(soup, category)

            # Parse text
            body_text = get_content(soup, category)

            # 创建blog并保存
            blog = Blog(url=url, website=website, title=title, author_id=author_id,
                        create_time=create_time, text=body_text)
            try:
                blog.save()
            except Exception as e:
                print(e)
                print(f"sino_{file_name} Blog 保存至数据库失败!")
                sys.exit(-1)
            else:
                print(f"sino_{file_name} Blog 保存至数据库成功!")

            # Parse image
            img_urls = get_img_urls(soup, category)

            # 列表不为空
            if len(img_urls) > 0:
                img_paths = []
                img_index = 0

                # 遍历所有url
                for img_url in img_urls:
                    response = requests.get(img_url, headers=headers)

                    # 404 Not Found
                    if response.status_code == 404:
                        print(f"sino_{file_name} 图片 {img_url} Not Found!")

                    #  200 OK
                    elif response.status_code == 200:
                        # 保存并记下路径
                        with open(f"blog/static/blog/images/sino/{file_name}_{img_index}.jpg", "wb") as img_file:
                            img_file.write(response.content)
                        img_paths.append(f"blog/static/blog/images/sino/{file_name}_{img_index}.jpg")
                        print(f"sino_{file_name} 图片 {img_index} OK!")
                        img_index += 1

                    # 出现问题
                    else:
                        # 这里不让程序终止是因为测试的时候有几个图片总是403,或者视频被当成了图片，好在这样的特例并不多
                        print(f"sino_{file_name} 图片 {img_url} Error!")
                        print(response)

                try:
                    # 保存图片
                    for img_path in img_paths:
                        img = Image(blog=blog, image_path=img_path)
                        img.save()
                except Exception as e:
                    print(e)
                    print(f"sino_{file_name} Image 保存至数据库失败!")
                    sys.exit(-1)
                else:
                    print(f"sino_{file_name} Image 保存至数据库成功!")
