class News:
    def __init__(self, url, title, author_id, author_img=None, fans=None, create_time=None, read_num=None, likes=None,
                 text=None, images=None):
        """
            初始化一条新闻
            :param url:str 链接
            :param title:str 标题
            :param author_id:str 作者id
            :param author_img:str 作者头像 (=None)
            :param fans:str 粉丝数 (=None)
            :param create_time:str 发布时间 (=None)
            :param read_num:str 阅读数 (=None)
            :param likes:str 点赞数 (=None)
            :param text:str 文章内容 (=None)
            :param images:dict {path:position} 图片链接 (=None)
        """
        self.url = url
        self.title = title
        self.author_id = author_id
        self.author_img = author_img
        self.fans = fans
        self.create_time = create_time
        self.read_num = read_num
        self.likes = likes
        self.text = text
        self.images = images

    def write_to_database(self):
        """
            将新闻写入数据库
        """
        pass

    def __str__(self):
        return f"url:{self.url} title:{self.title}"
