from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=140)

    class Meta:
        db_table = 'categories'


class Post(models.Model):

    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=False)
    text = models.TextField(null=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    published = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)

    class Meta:
        ordering = ('-pub_date', '-updated_at',)
        db_table = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=False)
    text = models.TextField(null=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_by = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    published = models.BooleanField(default=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'
