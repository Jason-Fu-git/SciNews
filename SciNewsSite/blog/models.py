from datetime import datetime

from django.db import models


class Blog(models.Model):
    """
    博客（新闻）模型，初始化时必须初始化的变量是:
    url - 网页链接
    website - 新闻网站
    title - 新闻网站
    author_id - 作者ID
    create_time - 创建时间
    text - 正文文字
    """
    url = models.URLField(max_length=100, unique=True)  # 网页链接
    website = models.CharField(max_length=20, default="")  # 新闻网站
    title = models.CharField(max_length=100)  # 新闻标题
    author_id = models.CharField(max_length=50)  # 作者ID
    author_img = models.CharField(max_length=100, blank=True)  # 作者头像，基本上都没有
    fans = models.IntegerField(default=0)  # 粉丝数，基本上都没有
    create_time = models.DateTimeField(blank=True)  # 创建时间
    read_num = models.IntegerField(default=0)  # 阅读量，基本上都没有
    likes = models.IntegerField(default=0)  # 点赞数，基本上都没有
    text = models.TextField(blank=True)  # 正文文字
    theme = models.CharField(max_length=20, default="")  # 主题

    def get_time_category(self):
        """
        获取时间分类
        :return: 时间分类： 1 - 近三月 | 2 - 近一年（不包括近三月） | 3 - 一年前
        """
        now = datetime.now()
        if (now - self.create_time).days <= 90:
            return 1
        elif (now - self.create_time).days <= 365:
            return 2
        return 3

    def __str__(self):
        return f"{self.title} | {self.author_id}"


class Image(models.Model):
    """
    图像模型，初始化时必须初始化的变量：
    blog - 关联的blog的id
    image_path - 图像路径，为相对于static/blog/images/的路径
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)  # 外键-博客（新闻）
    image_path = models.CharField(max_length=50)  # 图像路径

    def __str__(self):
        return f"{str(self.blog)} | {self.image_path}"


class Comment(models.Model):
    """
    评论模型，初始化时必须初始化的变量：
    blog - 关联的blog的id
    user_id - 用户名
    comment_content - 评论内容，非空
    发表时间自动填充，不可修改
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50)
    comment_content = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间,自动填充

    def __str__(self):
        return f"{str(self.blog)} | comment from {self.user_id}"


class Word(models.Model):
    """
    词模型，初始化时必须初始化的变量：
    blogs - 关联的blog的id，格式为 1,2,3,4
    word - 词
    frequency - 词频，默认为0
    dic_order - 字典序，主键
    """
    word = models.CharField(max_length=50)
    blogs = models.TextField()
    frequency = models.IntegerField(default=0)
    dic_order = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"{str(self.word)} | {self.blogs}"
