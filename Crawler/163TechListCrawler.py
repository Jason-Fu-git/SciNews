import requests
from bs4 import BeautifulSoup
import time

# 设置header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36 Edg/114.0.1823.67'}
# 目标url
url_ls = ["http://tech.163.com/special/gd2016/", "https://tech.163.com/special/5g_2019/",
          "https://tech.163.com/special/internet_2016/", "https://tech.163.com/special/tele_2016/",
          "https://tech.163.com/special/it_2016/", "https://tech.163.com/special/techscience/",
          "https://tech.163.com/special/metaverse_2022/"]
for i in range(2, 21):
    if i < 10:
        url_ls.append(f"http://tech.163.com/special/gd2016_0{i}/")
        url_ls.append(f"https://tech.163.com/special/5g_2019_0{i}/")
        url_ls.append(f"https://tech.163.com/special/internet_2016_0{i}/")
        url_ls.append(f"https://tech.163.com/special/tele_2016_0{i}/")
        url_ls.append(f"https://tech.163.com/special/it_2016_0{i}/")
        url_ls.append(f"https://tech.163.com/special/techscience_0{i}/")
        url_ls.append(f"https://tech.163.com/special/metaverse_2022_0{i}/")
    else:
        url_ls.append(f"http://tech.163.com/special/gd2016_{i}/")
        url_ls.append(f"https://tech.163.com/special/internet_2016_{i}/")
        url_ls.append(f"https://tech.163.com/special/tele_2016_{i}/")
        url_ls.append(f"https://tech.163.com/special/it_2016_{i}/")

url_ls.append("https://tech.163.com/special/5g_2019_10/")
url_ls.append("https://tech.163.com/special/techscience_10/")
url_ls.append(f"https://tech.163.com/special/metaverse_2022_10/")

links = []
# 共110页 1630条
for i in range(len(url_ls)):
    # 获取一页新闻
    response = requests.get(url_ls[i], params={}, headers=headers)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析文档
    links.extend([e.attrs['href'] for e in soup.find_all(class_="newsList-img", href=True)])  # 找到带有链接的元素并提取链接

    time.sleep(1)
    print(f"#{i + 1}:", url_ls[i], response)  # 监测状态

with open("../data/163_urls.txt", "w") as out_file:
    for link in set(links):  # 降重处理
        out_file.write(link)
        out_file.write("\n")
