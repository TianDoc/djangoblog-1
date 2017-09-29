from django.core.management.base import BaseCommand
from blog.cache_views import sync_article_views

class Command(BaseCommand):
    def handle(self, *args, **options):
		sync_article_views()