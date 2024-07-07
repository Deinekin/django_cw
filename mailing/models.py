from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(max_length=150, unique=True, verbose_name="Почта")
    name = models.CharField(max_length=150, verbose_name="Полное имя")
    comment = models.CharField(max_length=150, verbose_name="Комментарий", **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    message_title = models.CharField(max_length=150, verbose_name="Тема письма")
    message_body = models.TextField(verbose_name="Тело письма")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец рассылки",
                              **NULLABLE)

    def __str__(self):
        return f'{self.message_title}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    class Period(models.TextChoices):
        DAY = "D", "every day"
        WEEK = "W", "every week"
        MO = "M", "every month"

    class Status(models.TextChoices):
        CREATED = "C", "created"
        STARTED = "S", "started"
        FINISHED = "F", "finished"

    start_time = models.DateTimeField(verbose_name="Дата и время старта рассылки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания рассылки")
    period = models.CharField(max_length=10, choices=Period, default=Period.MO, verbose_name="Периодичность рассылки")
    status = models.CharField(max_length=10, choices=Status, default=Status.CREATED, verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, **NULLABLE, verbose_name="Сообщение рассылки")
    clients = models.ManyToManyField(Client, verbose_name="Клиенты рассылки")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="владелец", on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ('can_view_mailings', 'can view mailings')
        ]



class Log(models.Model):
    STATUS_MAILING = [
        ('Y', 'success'),
        ('N', 'fail'),
    ]

    date = models.DateTimeField(auto_now_add=True, verbose_name="дата отправки", **NULLABLE)
    status_mailing = models.CharField(max_length=2, choices=STATUS_MAILING, verbose_name="статус отправки", **NULLABLE)
    response = models.CharField(verbose_name="ответ сервера", **NULLABLE)
    mailing = models.ForeignKey(Mailing, verbose_name="рассылка", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.mailing} - {self.status_mailing}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"



