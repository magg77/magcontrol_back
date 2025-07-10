from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    nit = models.CharField(max_length=20, unique=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    cell = models.CharField(max_length=12)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
            
    def __str__(self):
        return self.company_name