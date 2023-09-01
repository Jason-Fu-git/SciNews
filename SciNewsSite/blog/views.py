from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from .models import Blog, Comment, Image, Word
import datetime
import time
import re


class DetailView(generic.DetailView):
    """新闻详情页"""
    template_name = 'blog/detail.html'  # 设置模板
    model = Blog  # 设置model
    blog = None

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, id=self.kwargs['pk'])  # 获取blog
        self.blog.read_num += 1  # 阅读量加1 （初始化时）
        self.blog.save()  # 保存更改
        return Blog.objects.filter(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        if self.blog is not None:  # 如果已经初始化就加一
            self.blog.read_num += 1
            self.blog.save()  # 保存更改
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = self.blog  # 将blog添加到上下文
        # 将图片添加至上下文
        context['images'] = Image.objects.filter(blog_id=self.blog.id)
        # 将评论添加至上下文
        context['comments'] = Comment.objects.filter(blog_id=self.blog.id)
        context['comments_num'] = len(context['comments'])
        # 判断评论是否为空,
        # 如果为空, 则添加提示信息
        if context['comments_num'] == 0:
            context['comments'] = [Comment(user_id="", comment_content="目前尚无用户发表评论", blog_id=self.blog.id)]
        # 时间分类
        time_cat = ["", "近三月", "近一年", "更早"]
        context['time_cat'] = time_cat[self.blog.get_time_category()]
        # 切割正文
        context['content'] = self.blog.text.split("\n")
        return context


def submit_commet(request, blog_id):
    """提交评论函数"""
    blog = get_object_or_404(Blog, pk=blog_id)  # 获取blog
    try:
        user_name = request.POST['user_name']  # 获取用户名
        comment_content = request.POST['comment_area']  # 获取评论内容

        # 没有评论内容直接返回
        if len(comment_content) == 0:
            return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': blog_id}))  # 重定向回详情页

        # 没有用户名则为“匿名用户”
        if len(user_name) == 0:
            user_name = "匿名用户"

    except Exception as e:
        print(e)
    else:
        # 将评论保存到数据库
        comment = Comment(user_id=user_name, comment_content=comment_content, blog_id=blog.id)
        comment.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': blog_id}))  # 重定向回详情页


class ListView(generic.ListView):
    """新闻列表视图"""
    model = Blog
    template_name = 'blog/list.html'
    context_object_name = 'blogs'
    paginate_by = 20  # 每页中对象数量

    def get_queryset(self):
        """获取新闻列表"""
        return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        #  获取评论数量
        comment_num_dic = {}
        for blog in context['blogs']:
            comment_num_dic[blog.id] = blog.comment_set.all().count()
        context['comment_num_dic'] = comment_num_dic

        # 获取正文前50个字符
        text_dic = {}
        for blog in context['blogs']:
            if len(blog.text) > 50:
                text_dic[blog.id] = blog.text[:50] + '...'
            else:
                text_dic[blog.id] = blog.text
        context['text_dic'] = text_dic

        return context


def list_to_page(request):
    """跳转至指定页面函数"""
    try:
        page = int(request.POST['page_number'])  # 获取页码
    except Exception as e:
        print(e)
        raise Http404('页面不存在')  # 抛出404错误
    else:
        return HttpResponseRedirect(reverse('blog:list_query', kwargs={'page': page}))  # 重定向回列表页


class IndexView(generic.ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = "blogs"

    def get_queryset(self):
        if Blog.objects.all().count() < 20:  # 小于20条，返回全部
            return Blog.objects.all()
        return Blog.objects.all().order_by('?')[:20]

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        #  获取评论数量
        comment_num_dic = {}
        for blog in context['blogs']:
            comment_num_dic[blog.id] = blog.comment_set.all().count()
        context['comment_num_dic'] = comment_num_dic

        # 获取正文前50个字符
        text_dic = {}
        for blog in context['blogs']:
            if len(blog.text) > 50:
                text_dic[blog.id] = blog.text[:50] + '...'
            else:
                text_dic[blog.id] = blog.text
        context['text_dic'] = text_dic

        return context


def on_search_submit(request):
    """处理首页搜索框提交的函数"""
    try:
        search_text = request.POST['search_input']  # 获取搜索框中内容
        order_choice = request.POST['order_group']  # 获取排序方式
        from_choice = '+'.join(request.POST.getlist('from_checkbox'))  # 获取分类“来源”
        time_choice = '+'.join(request.POST.getlist('time_checkbox'))  # 获取分类“时间”
    except Exception as e:
        print(e)
        return Http404('搜索过程出现错误')
    else:
        return HttpResponseRedirect(
            reverse('blog:search', kwargs={
                'content': f"text={search_text}&order={order_choice}&from={from_choice}&time={time_choice}"}))


class SearchView(generic.ListView):
    """搜索结果"""
    model = Blog
    template_name = 'blog/search.html'
    context_object_name = 'blogs'
    paginate_by = 20  # 每页中对象数量
    search_num = 0  # 条目数
    search_time_ms = 0  # 搜索耗时

    def get_queryset(self):
        begin_time = time.time()  # 搜索开始时间戳

        try:
            self.search_text = re.findall('text=([^&]+)', self.kwargs['content'])[0]  # 搜索文字
            self.order_choice = re.findall('order=([^&]+)', self.kwargs['content'])[0]  # 排序
            self.from_choice = re.findall('from=([^&]*)', self.kwargs['content'])[0]  # 来源
            self.time_choice = re.findall('time=([^&]*)', self.kwargs['content'])[0]  # 时间

            word = Word.objects.get(word=self.search_text)  # 精确匹配

        except Word.DoesNotExist:  # 如果不存在该词条
            end_time = time.time()  # 搜索结束时间戳
            self.search_time_ms = int(round((end_time - begin_time) * 1000))  # 搜索耗时（毫秒）

        else:
            # 按照分类筛选

            # 来源分类
            website_ls = []
            if '1' in self.from_choice:
                website_ls.append("网易新闻")
            if '2' in self.from_choice:
                website_ls.append("新浪新闻")
            if '3' in self.from_choice:
                website_ls.append("IT之家")
            if len(website_ls) == 0:  # 全部选中
                website_ls = ['网易新闻', '新浪新闻', 'IT之家']

            # 时间分类
            time_ls = self.time_choice.split('+')
            if len(time_ls) == 0:  # 全部选中
                time_ls = ['1', '2', '3']

            # 自定义Q, 用于时间分类筛选
            time_q = Q()
            for time_num in time_ls:
                if time_num == '1':
                    time_q |= Q(create_time__gte=datetime.datetime.now() - datetime.timedelta(days=90))
                elif time_num == '2':
                    time_q |= Q(create_time__lt=datetime.datetime.now() - datetime.timedelta(days=90),
                                create_time__gte=datetime.datetime.now() - datetime.timedelta(days=365))
                elif time_num == '3':
                    time_q |= Q(create_time__lt=datetime.datetime.now() - datetime.timedelta(days=365))

            blog_set = Blog.objects.filter(id__in=word.blogs.split(',')).filter(website__in=website_ls).filter(
                time_q)  # 获取符合要求的所有blog

            self.search_num = len(blog_set)  # 搜索结果条目数

            # 排序
            if self.order_choice == '1':
                blog_set = blog_set.order_by('-create_time')  # 按时间从新到旧排序
            elif self.order_choice == '2':
                blog_set = blog_set.order_by('-read_num')  # 按浏览量从高到低排序

            end_time = time.time()  # 搜索结束时间戳
            self.search_time_ms = int(round((end_time - begin_time) * 1000))  # 搜索耗时（毫秒）

            return blog_set

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        #  获取评论数量
        comment_num_dic = {}
        for blog in context['blogs']:
            comment_num_dic[blog.id] = blog.comment_set.all().count()
        context['comment_num_dic'] = comment_num_dic

        # 获取正文前50个字符
        text_dic = {}
        for blog in context['blogs']:
            if len(blog.text) > 50:
                text_dic[blog.id] = blog.text[:50] + '...'
            else:
                text_dic[blog.id] = blog.text
        context['text_dic'] = text_dic

        # 条目数
        context['search_num'] = self.search_num

        # 搜索耗时（毫秒）
        context['search_time_ms'] = self.search_time_ms

        # url中的content
        context['content'] = self.kwargs['content']

        # 搜索信息
        context['search_text'] = self.search_text
        context['order_choice'] = self.order_choice
        context['from_choice'] = self.from_choice.split('+')
        context['time_choice'] = self.time_choice.split('+')

        return context


def search_to_page(request, content):
    """跳转至指定页面函数"""
    try:
        page = int(request.POST['page_number'])  # 获取页码
    except Exception as e:
        print(e)
        raise Http404('页面不存在')  # 抛出404错误
    else:
        return HttpResponseRedirect(reverse('blog:search_page', kwargs={'content': content, 'page': page}))  # 重定向回列表页
