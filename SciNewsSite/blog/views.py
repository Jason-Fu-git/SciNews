from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from .models import Blog, Comment, Image


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


def to_page(request):
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
        if Blog.objects.all().count() < 20:
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
        search_text = request.POST['search_input']
        order_choice = request.POST['order_group']
        from_choice = request.POST.getlist('from_checkbox')
        time_choice = request.POST.getlist('time_checkbox')
    except Exception as e:
        print(e)
    else:
        print(search_text, order_choice, from_choice, time_choice)
