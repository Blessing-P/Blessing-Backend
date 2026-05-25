# customers/models.py

from django.db import models


class Customer(models.Model):
    name       = models.CharField(max_length=200)                          # Obligatorio
    telephone  = models.CharField(max_length=20, blank=True, null=True)
    nit        = models.CharField(max_length=20, blank=True, null=True)
    email      = models.EmailField(blank=True, null=True)
    address    = models.CharField(max_length=300, blank=True, null=True)
    is_active  = models.BooleanField(default=True)          

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering         = ['name']
        verbose_name     = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name