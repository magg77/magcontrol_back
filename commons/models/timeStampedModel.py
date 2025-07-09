from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)  # Fecha de creación
    updated_at = models.DateTimeField(default=timezone.now)# Fecha de última modificación

    class Meta:
        abstract = True  # No se crea una tabla para esta clase
