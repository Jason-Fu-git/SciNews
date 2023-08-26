import requests
import time
import re

# 设置header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36 Edg/114.0.1823.67'}

ls = []
# 读50页,共2500条
for i in range(1, 51):
    # 模拟request，获取该页数据
    response = requests.get(
        fr'https://feed.mix.sina.com.cn/api/roll/get?pageid=372&lid=2431&k=&num=50&page={i}'
        '&r=0.09298263416514674&callback=jQuery1112024828950400479521_1692967465967&_=1692967465971',
        params={},
        headers=headers)

    # 将返回的json数据写入列表
    response.encoding = 'UTF-8'
    html_txt = response.text
    ls.extend(re.findall('"url":\s*"(\S+?)"', html_txt))

    # 休眠两秒
    time.sleep(2)
    print(f"#{i}:", response)  # 打印状态

# 存入文件
with open("../data/sino_urls.txt", "w") as out_file:
    for news_url in ls:
        out_file.write(str(news_url).replace("\\", ""))  # strip the backslash
        out_file.write('\n')
