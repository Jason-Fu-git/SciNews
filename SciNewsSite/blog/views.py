from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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
        self.blog.save()
        return Blog.objects.filter(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        if self.blog is not None:  # 如果已经初始化就加一
            self.blog.read_num += 1
            self.blog.save()
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
