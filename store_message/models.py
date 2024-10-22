from django.db import models
from users.models import User, NULLABLE


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        abstract = True


class Store(BaseModel):
    theme = models.CharField(max_length=150, verbose_name='Тема сообщение')
    date_sanding = models.DateTimeField(verbose_name="Дата отправки", help_text='ДД.ММ.ГГГГ 00:00')
    date_receiving = models.DateTimeField(verbose_name="Дата получения", help_text='ДД.ММ.ГГГГ 00:00')
    description = models.TextField(verbose_name='Описание или текст сообщения')
    attachment = models.FileField(verbose_name='Вложение', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
