from django.db import models


# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=120)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ('-pub_date', '-updated')
        db_table = 'posts'

    def __str__(self):
        return self.title
