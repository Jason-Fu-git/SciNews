import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SciNewsSite.settings")
django.setup()

import jieba
from blog.models import Blog, Word


def separate():
    all_num = Blog.objects.count()
    count = 0
    # 使用 “结巴” 分词工具
    for blog in Blog.objects.all():
        punctuation_set = {"，", "。", "？", "！", "：", "、", "；", "“", "”", "（", "）", "《", "》", "【", "】", ",", ".", "?",
                           "!",
                           ":",
                           ";", "“", "”", "(", ")", "<", ">", "[", "]"}  # 常见标点列表（停用词）

        # 分词
        seg_list = set(jieba.cut_for_search(blog.title)).union(set(jieba.cut_for_search(blog.text))).difference(
            punctuation_set)  # 拼合标题正文、去除标点

        # 保存到数据库
        for word in seg_list:
            if not Word.objects.filter(word=word).exists():
                w = Word(word=word, blogs=str(blog.id), frequency=1)
                w.save()
            else:
                w = Word.objects.get(word=word)
                w.frequency += 1
                w.blogs += "," + str(blog.id)
                w.save()

        count += 1
        print("已处理：", count, "/", all_num, "Blog_id:", blog.id)


def order():
    # 按字典序排序
    words = Word.objects.all()
    words = sorted(words, key=lambda x: x.word)
    dic_id = 1
    for word in words:
        word.dic_order = dic_id
        word.save()
        dic_id += 1
        print(dic_id)
