from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Post, Category



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админ-панель модели статей"""
    prepopulated_fields = {"slug": ("title", )}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """Админ-панель модели категорий"""
    prepopulated_fields = {"slug": ("title", )}
