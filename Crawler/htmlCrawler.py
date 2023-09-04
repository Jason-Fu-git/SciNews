import sys
import time
import requests
import os

"""
html文件爬取
作者：付甲申
运行须知："../data/sino_urls.txt",  "../data/itHome_urls.txt", "../data/163_urls.txt" 三个文件务必存在
"../data/htmls/sino","../data/htmls/163","../data/htmls/itHome" 三个路径务必存在
"""

# 按照获取的url列表获取html文件

# 设置header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'}

# 网站-url列表字典
dic = {"sino": "../data/sino_urls.txt", "itHome": "../data/itHome_urls.txt", "163": "../data/163_urls.txt"}

for prefix, urls in dic.items():
    # load from url file:
    with open(urls, "r") as url_file:
        ls = [x for x in url_file.readlines() if "https" in x]
        print(f"start loading from{prefix}, length : {len(ls)}")
        for i in range(len(ls)):
            # get html file when the file doesn't exist
            if not os.path.exists(f"../data/htmls/{prefix}/{i}.html"):
                response = requests.get(str(ls[i]).strip(), headers=headers)
                if response.status_code == 200:  # OK
                    response.encoding = 'UTF-8'
                    # 将url对应的html文件下载到本地
                    with open(f"../data/htmls/{prefix}/{i}.html", "w") as out_file:
                        out_file.write(response.text)
                    print(f"{prefix}_{i} success!")
                elif response.status_code == 404:  # 404
                    # 无效链接，此种错误并不严重，故不导致程序终止。实验过程中大概遇到了50条无效链接
                    print(f"{prefix}_{i} 404 Not Found!")
                else:
                    # IP被封 等Bad Situation, 好在这几行代码没用到
                    print(f"Invalid quest at {prefix}_{i}")
                    sys.exit(i + 1)
                # 休眠1s，防止用到上面两行代码
                time.sleep(1)
