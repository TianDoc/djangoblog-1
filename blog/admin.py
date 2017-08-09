# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'img','categories','published_date','status','comments_count','view_count',]
    list_filter = ['published_date']
    earch_fields = ['title'] 
    actions = {'make_push','make_unpush',}
    #进行发布
    def make_push(self, request, queryset):
        try:
            for obj in queryset:
                if obj.status == 2:
                    res = queryset.update(status=1)
            self.message_user(request,'转为草稿成功')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '操作失败')
    make_push.short_description = "进行发布"
    #转为草稿
    def make_unpush(self, request, queryset):
        try:
            for obj in queryset:
                if obj.status == 1:
                    queryset.update(status=2)
            self.message_user(request,'发布成功')
        except Exception as e:
            messages.add_message(request, messages.ERROR, '操作失败')
    make_unpush.short_description = "转为草稿"

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Links)
# Register your models here.
