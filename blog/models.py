from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="заголовок")
    content = models.TextField(verbose_name="содержимое", **NULLABLE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    quantity_of_views = models.IntegerField(default=0, verbose_name="количество просмотров")

    def __str__(self):
        return f'{self.title}, {self.quantity_of_views}'

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"