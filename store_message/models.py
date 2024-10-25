from django.db import models
from users.models import User, NULLABLE


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        abstract = True


class EmailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Аккаунт электронной почты'
        verbose_name_plural = 'Аккаунты электронной почты'


class Store(BaseModel):
    theme = models.CharField(max_length=150, verbose_name='Тема сообщение')
    date_sanding = models.DateTimeField(verbose_name="Дата отправки", help_text='ДД.ММ.ГГГГ 00:00', **NULLABLE)
    date_receiving = models.DateTimeField(verbose_name="Дата получения", help_text='ДД.ММ.ГГГГ 00:00')
    description = models.TextField(verbose_name='Описание или текст сообщения')
    attachment = models.FileField(verbose_name='Вложение', **NULLABLE)
    # account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
