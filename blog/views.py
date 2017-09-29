# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.shortcuts import render, redirect, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .models import *
from django.http import HttpResponse
import collections
from django.views.decorators.cache import cache_page
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse


# 引入缓存（redis）
from django.core.cache import cache
from django_redis import get_redis_connection
REDIS_DB = get_redis_connection('default')

# from django_redis import get_redis_connection
# REDIS_DB = get_redis_connection('default')
# 引入jieba分词
import jieba
import jieba.analyse
# 引入haystack搜索
from haystack.query import SearchQuerySet

from django.views.decorators.csrf import csrf_exempt

from .cache_views import update_article_views,get_article_views
# 引入日志模块
import logging

# 每页数
PAGE_SIZE = settings.PAGE_SIZE

# 测试
# @cache_page(60 * 30)
# def test(request):
#     try:
#         #首页文章列表数据(已发布)
#         article_list = Article.objects.filter(status=1).values('id','title','published_date','user','desc','img').order_by('-published_date')
#         #进行分页处理
#         page = request.GET.get('page', 1)
#         article_list = get_page(request, article_list,int(page))
#     except Exception as e:
#         logging.error(e)
#     return render(request, 'test.html',{"article_list":article_list})

# 分页处理
# 分页处理
def get_page(request,article_list,page):
    paginator = Paginator(article_list, PAGE_SIZE)  # 一页最多显示4篇文章
    try:
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)  #出现异常就返回第一页
    return article_list

# 首页
def index(request):
	try:
		article_list = Article.objects.filter(status=1).values('id', 'title', 'published_date', 'user', 'desc', 'img').order_by('-published_date')
		# 进行分页处理
		page = request.GET.get('page', 1)
		article_list = get_page(request, article_list, int(page))
	except Exception as e:
		logging.error(e)
	return render(request, 'list.html', {"article_list": article_list})


# 根据分类获取文章列表
def article_list_by_category(request, catid):
	try:
		article_list = Article.objects.filter(categories=int(catid), status=1).values('id', 'title', 'published_date','user', 'desc', 'img')
		if article_list:
			page = request.GET.get('page', 1)
			article_list = get_page(request, article_list, int(page))
		else:
			return render(request, 'failure.html', {'reason': '该分类下暂无内容！'})
	except Exception as e:
		logging.error(e)
	return render(request, 'list.html', {"article_list": article_list})


# 根据tag获取文章列表
def article_list_by_tag(request, tagid):
	try:
		try:
			tag = Tag.objects.get(id=int(tagid))
		except Exception as e:
			return render(request, 'failure.html', {'reason': '您访问的标签不存在！'})
		article_list = tag.article_set.filter(status=1).values('id', 'title', 'published_date', 'user', 'desc', 'img')
		if article_list:
			page = request.GET.get('page', 1)
			article_list = get_page(request, article_list, int(page))
		else:
			return render(request, 'failure.html', {'reason': '该标签下暂无内容！'})
	except Exception as e:
		logging.error(e)
	return render(request, 'list.html', {"article_list": article_list})


# 根据文章id获取文章详情
def article(request, id):
	try:
		# 获取文章信息
		try:
			article = Article.objects.get(id=int(id))
			#return HttpResponse(article.content)
			article.view_count = get_article_views(article.id, article.view_count)
			article_info_tags = article.tags.all()
			# 获取文章信息
			# key = 'article/' + id
			# article = REDIS_DB.get(key)
			# if not article:
			# 	article = Article.objects.get(id=int(id))
			# 	return HttpResponse(article.content)
			# 	article.view_count = get_article_views(article.id, article.view_count)
			# 	article_info_tags = article.tags.all()
			# 	REDIS_DB.set(key+'/tags', article_info_tags, 10)
			# 	REDIS_DB.set(key, article, 10)
			# else:
			# 	article.view_count = get_article_views(article.id, article.view_count)
			# 	article_info_tags = REDIS_DB.get(key+'/tags')
		except Article.DoesNotExist:
			return render(request, 'failure.html', {'reason': '没有找到对应的文章！'})
		# 点击量+1
		# article.view_count += 1
		# article.save()
		update_article_views(article.id, article.view_count)
		# 文章相关的tag

	except Exception as e:
		logging.error(e)
	return render(request, 'article.html', {'article': article, 'article_info_tags': article_info_tags})


# 关于静态页
@cache_page(3600)
def about(request):
	return render(request, 'about.html')


# 留言
def comment(request):
	return render(request, 'comment.html')


# 归档
@cache_page(3600)
def archive(request):
	try:
		date_list = collections.defaultdict(list)
		article_archive = Article.objects.values('id', 'title', 'published_date').order_by('-published_date')
		for art in article_archive:
			year = str(art['published_date'].strftime('%Y'))
			# return HttpResponse(year)
			month = str(art['published_date'].strftime('%m'))
			art['time'] = year + '-' + month
			if month not in date_list[year]:
				date_list[year].append(month)
		# 对数据进行倒叙操作
		date_list = sorted(date_list.items(), reverse=True)
	except Exception as e:
		logging.error(e)
	# return HttpResponse(date_list)
	return render(request, 'archive.html', {'article_archive': article_archive, 'date_list': date_list})


# 订阅
class RSSFeed(Feed):
	title = "朽小蜗"
	link = "feed/"
	description = "欢迎订阅朽小蜗的博文！"

	def items(self):
		return Article.objects.order_by('-published_date')

	def item_title(self, item):
		return item.title

	def item_pubdate(self, item):
		return item.published_date

	def item_description(self, item):
		return item.desc[0:30] + '...'

	def item_link(self, item):
		return reverse('article', args=[item.id])


# 全局搜索
def full_search(request):
	try:
		keywords = request.GET['q']
		article_list = []
		# 将要查询的内容，进行分词处理，去权重最高的词（最多3个）
		search_model = jieba.analyse.extract_tags(keywords, 3)
		for key in search_model:
			# 为提高查询效率，只查询前100条
			results = SearchQuerySet().filter(content=key)
			for res in results:
				if res.object not in article_list:
					article_list.append(res.object)
	except Exception as e:
		logging.error(e)
	return render(request, 'search.html', {"article_list": article_list, 'keywords': keywords})


# 错误处理404和500页面
@csrf_exempt
def page_not_found(request):
	return render(request, 'failure.html', {'reason': '您访问的页面不存在！'})


@csrf_exempt
def page_error(request):
	return render(request, 'failure.html', {'reason': '您访问的页面不存在！'})
