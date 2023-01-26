from django.db import models
from django.utils import timezone

from network.models.contact import Contact
from network.models.products import Products


class Basic(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(verbose_name='Название', max_length=255)
    contacts = models.ForeignKey(Contact, verbose_name='Контакты', on_delete=models.PROTECT)
    products = models.ForeignKey(Products, verbose_name='Продукт', on_delete=models.PROTECT)
    debt = models.FloatField(verbose_name='Задолженность перед поставщиком')
    created = models.DateTimeField(verbose_name='Дата создания')
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title