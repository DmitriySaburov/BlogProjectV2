from django.contrib import admin

from .models import Profile



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админ-панель модели профилей"""
    
    list_display = ("user", "birth_date", "slug")
    list_display_links = ("user", "slug")
