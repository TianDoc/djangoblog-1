from django.conf.urls import url
from blog.views import *
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    'static': StaticViewSitemap,
    'blog': GenericSitemap({'queryset': Article.objects.all(), 'date_field': 'published_date'}, priority=0.6),

}
# sitemaps = {
#     'blog': GenericSitemap({'queryset': Article.objects.all(), 'date_field': 'published_date'}, priority=0.6),
# }

urlpatterns = [
    url(r'^article/category/(?P<catid>\d+)$',article_list_by_category,name='arts_by_category'),
    url(r'^article/tag/(?P<tagid>\d+)$',article_list_by_tag, name='arts_by_tag'),    
    url(r'^article/(?P<id>\d+)$',article, name='article'),
    url(r'^about/$',about, name='about'),
    url(r'^archive/$',archive, name='archive'),
    url(r'^$',index, name='index'),
    #url(r'^test/$',test, name='test'),
    url(r'^feed/$',RSSFeed(), name = 'feed'),
    #url(r'^search/', include('haystack.urls')),
    url(r'^search/', full_search,name='search'),
    url(r'^comment/$',comment, name='comment'),
    url(r'^sitemap\.xml$', cache_page(86400)(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]
