from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

from apps.services.utils import unique_slugify



class PostManager(models.Manager):
    """Менеджер для модели статей"""
    
    def get_queryset(self):
        """Список только опубликованных постов. Используем select_related() чтобы сразу запросить необходиммые связанные данные"""
        return super().get_queryset().select_related("author", "category").filter(status="published")
    

class Post(models.Model):
    """Модель статей для блога"""
    
    STATUS_OPTIONS = (("published", "Опубликовано"), ("draft", "Черновик"))
    
    title = models.CharField(
        verbose_name="Название статьи",
        max_length=255
    )
    slug = models.SlugField(
        verbose_name="URL статьи",
        max_length=255,
        blank=True,
        unique=True
    )
    description = RichTextField(
        config_name='awesome_ckeditor',
        verbose_name="Краткое описание статьи",
        max_length=500
    )
    text = RichTextField(
        config_name='awesome_ckeditor',
        verbose_name="Полный текст статьи"
    )
    category = TreeForeignKey(
        "Category",
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="posts"
    )
    thumbnail = models.ImageField(
        verbose_name="Изображение статьи",
        default="default.jpg",
        blank=True,
        upload_to="images/thumbnails/%Y/%m/%d/",
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
    create = models.DateTimeField(
        verbose_name="Время добавления",
        auto_now_add=True
    )
    update = models.DateTimeField(
        verbose_name="Время обновления",
        auto_now=True
    )
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
    fixed = models.BooleanField(
        verbose_name="Прикреплено",
        default=False
    )
    
    # менеджеры
    objects = models.Manager()
    published = PostManager()
    tags = TaggableManager()
    
    class Meta:
        db_table = "blog_post"
        ordering = ["-fixed", "-create"]
        indexes = [models.Index(fields=["-fixed", "-create", "status"])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
    
    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        """Переопределили метод save. При сохранении статьи генерируем slug и проверяем на уникальность"""
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)
        
    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])
    


class Category(MPTTModel):
    """Модель категорий с вложенностью"""
    
    title = models.CharField(verbose_name="Название категории", max_length=255)
    slug = models.SlugField(verbose_name="URL категории", max_length=255, blank=True)
    description = models.TextField(verbose_name="Описание категории", max_length=300)
    parent = TreeForeignKey(
        "self",
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name="children"
    )
    
    class MPTTMeta:
        """Сортировка по вложенности"""
        order_insertion_by = ("title", )
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "app_categories"
    
    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("post_by_category", kwargs={"slug": self.slug})


class Comment(MPTTModel):
    """Модель древовидных комментариев"""
    
    STATUS_OPTIONS = (
        ("published", "Опубликовано"),
        ("draft", "Черновик")
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Запись',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments_author'
    )
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(
        choices=STATUS_OPTIONS,
        default='published',
        verbose_name='Статус комментария',
        max_length=10
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    
    class MPTTMeta:
        """Сортировка по вложенности"""
        order_insertion_by = ("-time_create", )
    
    class Meta:
        """Сортировка, название модели в админке, таблица с данными"""
        ordering = ["-time_create"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
    
    def __str__(self):
        return f"{self.author}:{self.content}"


class Rating(models.Model):
    """Модель рейтинга: Лайк / Дизлайк"""
    
    post = models.ForeignKey(
        to=Post,
        verbose_name="Запись",
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    user = models.ForeignKey(
        to=User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    value = models.IntegerField(
        verbose_name="Значение",
        choices=[(1, "Нравится"), (-1, "Не нравится")]
    )
    time_create = models.DateTimeField(
        verbose_name="Время добавления",
        auto_now_add=True
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP Адрес"
    )
    
    class Meta:
        unique_together = ("post", "ip_address")
        ordering = ("-time_create", )
        indexes = [models.Index(fields=["-time_create", "value"])]
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        
    def __str__(self):
        return f"{self.post.title}"
