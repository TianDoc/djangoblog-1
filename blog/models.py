# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
import collections
import json
from django.core.urlresolvers import reverse
#标签模型
class Tag(models.Model):  
    name = models.CharField(max_length=30, verbose_name='标签名称')  
    sort = models.SmallIntegerField(verbose_name='分类排序',default=1)

    class Meta:  
        verbose_name = '标签'  
        verbose_name_plural = verbose_name  
        ordering = ['sort']

    def __unicode__(self):  
        return self.name  

#分类模型
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称') #分类名称 
    sort = models.SmallIntegerField(verbose_name='分类排序',default=1)  #排序 
    pid = models.ForeignKey('self', blank=True, null=True,verbose_name='父级评论')

    class Meta:  
        verbose_name = '分类'  
        verbose_name_plural = verbose_name  
        ordering = ['sort']

    def __unicode__(self):  
        return self.name 

# 自定义一个文章Model的管理器
# 1、新加一个数据处理的方法
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = collections.defaultdict(list)
        date_list = self.values('published_date').order_by('published_date')
        for date in date_list:
            y = date['published_date'].strftime('%Y')
            m = date['published_date'].strftime('%m')
            date = date['published_date'].strftime('%Y/%m')
            if date not in distinct_date_list:
                art_list =self.filter(published_date__year=y,published_date__month=m).values('id','title','published_date').order_by('-published_date')
                for art in art_list:
                    distinct_date_list[date].append(art)
        return distinct_date_list

#文章模型
class Article(models.Model):
    # 文章发布状态
    CONTENT_STATUS_PUBLISHED = 1
    # 文章草稿箱状态
    CONTENT_STATUS_DRAFT = 2
    # 文章状态选项
    CONTENT_STATUS_CHOICES = (
        (CONTENT_STATUS_PUBLISHED, '发布'),
        (CONTENT_STATUS_DRAFT, '草稿箱'),
    )
    
    IMG_IS_SHOW = (
        (1, '展示'),
        (0, '不展示'),
    )

    title = models.CharField(verbose_name ='标题', max_length=100)
    user = models.CharField(verbose_name ='作者',max_length=50)
    img = models.ImageField(upload_to='article/',verbose_name='首页展示图片')
    img_is_centent_show = models.SmallIntegerField(verbose_name='首页图片是否在文章顶端展示', default=0, choices=IMG_IS_SHOW)
    desc = models.TextField(verbose_name ='摘要',blank=True)
    content = models.TextField(verbose_name ='文章内容')
    categories = models.ForeignKey(Category,verbose_name ='分类')
    tags = models.ManyToManyField(Tag, blank=True,
                                        verbose_name = '标签'
                                        )
    published_date = models.DateTimeField(verbose_name ='发布时间',blank=True, null=True)    # 发表时间
    status = models.IntegerField(verbose_name ='状态',
                                 choices=CONTENT_STATUS_CHOICES,
                                 default=CONTENT_STATUS_PUBLISHED)      # 状态：1为正式发布，2为草稿箱
    comments_count = models.IntegerField(verbose_name ='评论数',default=0)     # 评论总数
    view_count = models.IntegerField(verbose_name ='浏览数',default=0)         # 浏览总数

    objects = ArticleManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('article',args=[self.pk])
        
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_date']

    def __unicode__(self):
        return self.title


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排序')
    examination = models.BooleanField(default=False, verbose_name='是否审核通过')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __unicode__(self):
        return self.title

#评论
class Comment(models.Model):
    nickname = models.CharField(max_length=30, verbose_name='评论者昵称')
    mail = models.EmailField(verbose_name='评论者邮箱',max_length=255)
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(verbose_name='评论发表时间', auto_now_add=True)
    pid = models.IntegerField(default=0, verbose_name='父级id')
    module_id = models.IntegerField(default=0, verbose_name='模块下内容的id')
    module = models.CharField(max_length=30,verbose_name ='所属模块')