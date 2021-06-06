from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class PublishedManager(models.Model):
    """Менеджер модели"""

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    """Модель хранения данных для постов"""

    objects = models.Manager()  # Менеджер по умолчанию
    published = PublishedManager()  # Мой менеджер
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=255, verbose_name="Название поста")
    slug = models.SlugField(max_length=255, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField(verbose_name="Текст поста")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month,
                                                 self.publish.day, self.slug])

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель хранения данных для комментариев"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "Комментарий от {} к {}".format(self.name, self.post)
