from django.db import models

class Guest(models.Model):
    name = models.CharField(max_length=255)
    name_companions = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_attending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {'Confirmado' if self.is_attending else 'Pendente'}"
