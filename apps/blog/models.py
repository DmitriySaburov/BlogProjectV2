from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User



class Post(models.Model):
    """Модель статей для блога"""
    
    STATUS_OPTIONS = (("published", "Опубликовано"), ("draft", "Черновик"))
    
    title = models.CharField(verbose_name="Название статьи", max_length=255)
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True, unique=True)
    description = models.TextField(verbose_name="Краткое описание статьи", max_length=500)
    text = models.TextField(verbose_name="Полный текст статьи")
    thumbnail = models.ImageField(
        verbose_name="Изображение статьи",
        default="default.jpg",
        blank=True,
        upload_to="images/thumbnails/",
        validators=[
            FileExtensionValidator(allowed_extensions=("png", "jpg", "webp", "jpeg", "gif"))
        ]
    )
    status = models.CharField(
        verbose_name="Статус статьи",
        choices=STATUS_OPTIONS,
        default="published",
        max_length=10
    )
    create = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)
    update = models.DateTimeField(verbose_name="Время обновления", auto_now=True)
    author = models.ForeignKey(
        verbose_name="Автор",
        to=User,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="author_posts"
    )
    updater = models.ForeignKey(
        verbose_name="Обновил",
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updater_posts"
    )
    fixed = models.BooleanField(verbose_name="Прикреплено", default=False)
    
    class Meta:
        db_table = "blog_post"
        ordering = ["-fixed", "-create"]
        indexes = [models.Index(fields=["-fixed", "-create", "status"])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
    
    def __str__(self):
        return f"{self.title}"
