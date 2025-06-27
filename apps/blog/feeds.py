from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Post



class LatestPostFeed(Feed):
    title = "Последние записи"
    link = "/feeds/"
    description = "Новые записи на сайте."
    
    def items(self):
        return Post.published.order_by("-update")[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return item.get_absolute_url()