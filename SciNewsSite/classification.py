# 从文章正文中提取关键词
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SciNewsSite.settings")
django.setup()

import jieba.analyse
from blog.models import Blog, Word
import pandas


def extract_keywords():
    # 利用pandas dataframe存储关键词
    df = pandas.DataFrame(columns=["kw", 'weight', 'blog_id'])

    for blog in Blog.objects.all():
        text = blog.text

        # 关键词提取
        tags = jieba.analyse.extract_tags(text, topK=7, withWeight=True)
        if len(tags) == 7:  # 存在有的文章较短的情况
            for i in range(7):
                tags[i] += (blog.id,)

            # pandas 存储关键词
            temp = pandas.DataFrame(tags, columns=["kw", 'weight', 'blog_id'])
            df = df.append(temp, ignore_index=True)

        print("complete: ", blog.id)

    df.to_csv("keywords.csv", index=False)
    print('success!')


# 根据提取到的关键词手动分类
def blog_theme_classify():
    product_ls = ['手机', '华为', '三星', '荣耀', '小米', '微软', 'GB', 'TB', '处理器', 'CPU', 'GPU', '英伟达',
                  '英特尔', 'intel', 'nvidia', '内存', 'huawei', 'galaxy', 'microsoft', '苹果', 'apple', 'arm', '产品',
                  '软件', '硬件']
    ai_ls = ["AI", "ChatGPT", "人工智能", "文心", '大模型', 'NLP', 'GPT', 'Transformer', 'chatgpt', '机器学习',
             '深度学习']
    finance_ls = ['股票', '基金', '期货', '上涨', '下跌', '业务', '收入', '股市', '金融', '财经']

    # 顺序不能改变

    # ‘科技产品’类
    for kw in product_ls:
        words = Word.objects.filter(word__iexact=kw)
        if words.count() != 0:
            for word in words:
                blogs = word.blogs.split(',')
                for blog_id in blogs:
                    blog = Blog.objects.get(id=int(blog_id))
                    blog.theme = '科技产品'
                    blog.save()

    print('科技产品类分类完成！')

    # ‘财经’类
    for kw in finance_ls:
        words = Word.objects.filter(word__iexact=kw)
        if words.count() != 0:
            for word in words:
                blogs = word.blogs.split(',')
                for blog_id in blogs:
                    blog = Blog.objects.get(id=int(blog_id))
                    blog.theme = '财经'
                    blog.save()
    print('财经类分类完成！')

    # ‘人工智能’类
    for kw in ai_ls:
        words = Word.objects.filter(word__iexact=kw)
        if words.count() != 0:
            for word in words:
                blogs = word.blogs.split(',')
                for blog_id in blogs:
                    blog = Blog.objects.get(id=int(blog_id))
                    blog.theme = 'AI'
                    blog.save()
    print('AI类分类完成！')

    # ‘其他’
    for blog in Blog.objects.all():
        if blog.theme is None:
            blog.theme = '其他'
            blog.save()
        else:
            if blog.theme == '':
                blog.theme = '其他'
                blog.save()
    print('其他类分类完成！')


extract_keywords()
