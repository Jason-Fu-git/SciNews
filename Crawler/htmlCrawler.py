import sys
import time
import requests
import os

# 按照获取的url列表获取html文件

# 设置header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'}

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
                    with open(f"../data/htmls/{prefix}/{i}.html", "w") as out_file:
                        out_file.write(response.text)
                    print(f"{prefix}_{i} success!")
                elif response.status_code == 404:  # 404
                    print(f"{prefix}_{i} 404 Not Found!")
                else:
                    print(f"Invalid quest at {prefix}_{i}")
                    sys.exit(i + 1)
                time.sleep(1)
