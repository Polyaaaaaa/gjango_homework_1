from django.db import models


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.CharField(max_length=150, verbose_name='Содержимое')
    preview = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to='blog/')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    publication_sign = models.BooleanField(default=False, blank=True)
    number_of_views = models.IntegerField(verbose_name='Стоимость', blank=True, default=0)


    def __str__(self):
        return f"{self.title} {self.content}"

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['title', 'content', 'created_at', 'number_of_views']
