from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from debug_toolbar.toolbar import debug_toolbar_urls

from apps.blog.feeds import LatestPostFeed



handler403 = "apps.blog.views.tr_handler403"
handler404 = "apps.blog.views.tr_handler404"
handler500 = "apps.blog.views.tr_handler500"

urlpatterns = [
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('admin/', admin.site.urls),
    path("feeds/latest/", LatestPostFeed(), name="latest_post_feed"),
    path("", include("apps.blog.urls")),
    path("", include("apps.accounts.urls")),
]

# в режиме отладки добавляем медиа и статик
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
# в режиме отладки добавляем маршрут для работы дебагера
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
