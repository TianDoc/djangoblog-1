# -*- coding: utf-8 -*-
from django.conf import settings 
from blog.models import *
from django.db.models import Count

from django_redis import get_redis_connection
REDIS_DB = get_redis_connection('default')

def get_contcats(request):
    contcat_list = [
        {'name':'github','url':'https://github.com/akcj'},
        {'name':'微博','url':'https:weibo.com/u/3538915371?is_all=1'},
        {'name':'知乎','url':'https://www.zhihu.com/people/xiu-xiao-gua/activities'},
    ]
    return {'contcat_list':contcat_list}
#获取全局配置文件
def get_setting(request):
    return {'MEDIA_URL': settings.MEDIA_URL,
            'ARTICLE_THUMB':settings.ARTICLE_THUMB,
            'SITE_URL':settings.SITE_URL,
            'SITE_NAME':settings.SITE_NAME,
            'SITE_DESC':settings.SITE_DESC,
            'SITE_SEO_DESCRIPTION':settings.SITE_SEO_DESCRIPTION,
            'SITE_SEO_KEYWORDS':settings.SITE_SEO_KEYWORDS,
            }
#点击排行
def art_list_by_view(request):
    views_list = Article.objects.filter(status=1).values('id','title','img','published_date').order_by('-view_count')[:4]
    return {'views_list': views_list}
#全部文章分类
def get_all_category(request):
    article_categorys = Category.objects.order_by('sort').filter(pid_id=1).annotate(
    num_articles=Count('article')).filter(num_articles__gt=0)
    return {'article_categorys': article_categorys}
#所有标签
def get_all_tag(request):
    all_tags = Tag.objects.order_by('sort').filter().annotate(num_articles=Count('article')).filter(num_articles__gt=0)[0:16]
    return {'all_tags': all_tags}
