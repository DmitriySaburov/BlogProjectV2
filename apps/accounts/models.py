from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.cache import cache
from django.urls import reverse

from apps.services.utils import unique_slugify



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(
        verbose_name="URL профиля",
        max_length=255,
        blank=True,
        unique=True
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="images/avatars/%Y/%m/%d/",
        default="images/avatars/default.png",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg", "jpeg"))]
    )
    bio = models.TextField(verbose_name="Информация о себе", max_length=500, blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    
    class Meta:
        ordering = ("user", )
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def save(self, *args, **kwargs):
        """Автозаполнение поля slug"""
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username, self.slug)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}"
    
    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"slug": self.slug})
    
    def is_online(self):
        cache_key = f"last-seen-{self.user.id}"
        last_seen = cache.get(cache_key)
        if last_seen is not None:
            return True
        return False
