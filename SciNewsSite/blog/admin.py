from django.contrib import admin

from .models import Blog, Image, Comment


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic information", {
            "fields": ["title", "url", "create_time", "website"]
        }),
        ("Author information", {
            "fields": ["author_id", "author_img", "fans"]
        }),
        ("Content", {
            "fields": ["text"]
        }),
        ("Others", {
            "fields": ["read_num", "likes"]
        })
    ]


# Register models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Image)
admin.site.register(Comment)
