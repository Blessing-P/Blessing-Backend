# apps/catalog/models.py

from django.db import models


class Category(models.Model):
    TYPE_CHOICES = [
        ('product', 'Producto'),
        ('supply',  'Insumo'),
    ]

    name      = models.CharField(max_length=100, unique=True)
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta:
        ordering            = ['name']
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return f'{self.name} ({self.item_type})'


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering            = ['name']
        verbose_name        = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.name