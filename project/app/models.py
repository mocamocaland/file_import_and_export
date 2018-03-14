from datetime import datetime
from django.db import models


class Category(models.Model):
    
    name = models.CharField('カテゴリ名', max_length=255)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField('タイトル', max_length=255)
    text = models.TextField('本文', max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリ', null=True)

    def __str__(self):
        return self.title
