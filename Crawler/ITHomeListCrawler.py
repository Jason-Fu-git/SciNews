import requests
from bs4 import BeautifulSoup
import time
from datetime import date, timedelta

# 设置header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36 Edg/114.0.1823.67'}
# 目标url, 按日期获取前半年的新闻（每隔一周获取一次）
url_ls = []
begin = date(2023, 1, 1)
end = date(2023, 6, 30)
while begin <= end:
    day_str = begin.strftime('%Y-%m-%d')
    url_ls.append(f"https://www.ithome.com/list/{day_str}.html")
    begin += timedelta(days=7)
links = []

# 共2626条
for i in range(len(url_ls)):
    # 获取一页新闻
    response = requests.get(url_ls[i], params={}, headers=headers)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析文档
    links.extend([e.attrs['href'] for e in soup.find_all(class_="t", href=True)])  # 找到带有链接的元素并提取链接

    time.sleep(1)
    print(f"#{i + 1}:", url_ls[i], response)  # 监测状态

with open("../data/itHome_urls.txt", "w") as out_file:
    for link in links:
        if "https://www.ithome.com/" in str(link):
            out_file.write(link)
            out_file.write("\n")
