from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return self.title
