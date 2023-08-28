import os
import sys

import django
import re
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SciNewsSite.settings")
django.setup()

from blog.models import Blog, Image, Comment
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'}

'''
网易新闻解码器
作者：付甲申
'''

# 获取所有html文件名
fs = []
for root, dirs, files in os.walk("../data/htmls/163"):
    for file in files:
        fs.append(str(re.findall("(.*)\.html", file)[0]))

print(f"start loading {len(fs)} files")
# 开始遍历
for file_name in fs:
    # 读取html文件

    with open(f"../data/htmls/163/{file_name}.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

        # Parse url
        url = soup.find("meta", property="og:url")["content"]

        # 避免重复
        try:
            Blog.objects.get(url=str(url))
        except Blog.DoesNotExist: # 这里使用try-except块，是因为url不存在时会抛出Blog.DoesNotExist异常，利用这个异常可以避免重复添加
            # Parse title
            title = soup.find("h1", class_="post_title").text
            website = "网易新闻"

            # Parse time and author
            info = soup.find("div", class_="post_info").text
            author_id = re.findall("来源[:：]\s*(\S+)", info)[0]
            create_time = datetime.strptime(re.findall("\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}", info)[0]
                                            , "%Y-%m-%d %H:%M:%S") # 转化为 datetime 格式

            # Parse text
            body_texts = [str(p.text).replace("\n", "").replace(" ", "") for p in
                          soup.find("div", class_="post_body").find_all("p")] # 列表形式的正文
            body_text = ""
            for text in body_texts:
                body_text += text + "\n" # 压缩为字符串

            # 创建blog并保存
            blog = Blog(url=url, website=website, title=title, author_id=author_id,
                        create_time=create_time, text=body_text)
            try:
                blog.save()
            except Exception as e:
                print(e)
                print(f"163_{file_name} Blog 保存至数据库失败!")
                sys.exit(-1)
            else:
                print(f"163_{file_name} Blog 保存至数据库成功!")

                # Parse image
            ps = [p for p in soup.find("div", class_="post_body").find_all("p", class_="f_center")
                  if p.img is not None]

            # 图像列表不为空
            if len(ps) > 0:
                img_urls = [p.img["src"] for p in ps]
                img_paths = []
                img_index = 0

                # 遍历所有url
                for img_url in img_urls:
                    response = requests.get(img_url, headers=headers)

                    # 404 Not Found
                    if response.status_code == 404:
                        print(f"163_{file_name} 图片 {img_url} Not Found!")

                    #  200 OK
                    elif response.status_code == 200:
                        # 保存图片并记下路径
                        with open(f"blog/static/blog/images/163/{file_name}_{img_index}.jpg", "wb") as img_file:
                            img_file.write(response.content)
                        img_paths.append(f"blog/static/blog/images/163/{file_name}_{img_index}.jpg")
                        print(f"163_{file_name} 图片 {img_index} OK!")
                        img_index += 1

                    # 出现问题
                    else:
                        print(f"163_{file_name} 图片 {img_url} Error!")
                        print(response)

                try:
                    # 保存图片
                    for img_path in img_paths:
                        img = Image(blog=blog, image_path=img_path)
                        img.save()
                except Exception as e:
                    print(e)
                    print(f"163_{file_name} Image 保存至数据库失败!")
                    sys.exit(-1)
                else:
                    print(f"163_{file_name} Image 保存至数据库成功!")
