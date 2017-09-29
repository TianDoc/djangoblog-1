# -*-coding:utf-8 -*-

from django.conf import settings
from .models import *
from django_redis import get_redis_connection
REDIS_DB = get_redis_connection('default')

#在redis上更新文章点击量
def update_article_views(id,article_views):
	key = 'article_views_count'
	if REDIS_DB.hexists(key, id):
		REDIS_DB.hincrby(key, id)
	else:
		REDIS_DB.hset(key, id, article_views + 1)

#从redis获取文章点击量
def get_article_views(id,article_views):
	key = 'article_views_count'
	if REDIS_DB.hexists(key,id):
		article_views = REDIS_DB.hget(key,id)
		return article_views
	else:
		REDIS_DB.hset(key,id,article_views)
		return article_views

#同步文章点击量
def sync_article_views():
	key = 'article_views_count'
	for k in REDIS_DB.hkeys(key):
		try:
			article = Article.objects.get(pk=int(k))
			view_count = get_article_views(article.id,article.view_count)
			if article.view_count != view_count:
				article.view_count = view_count
				article.save()
		except:
			pass


