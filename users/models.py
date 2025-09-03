from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Suppression de CompanyManager et Company


class Customer(AbstractUser):
    roles = [
        ('simple' ,'Simple'),
        ('admin', 'ADMINISTRATEUR')
    ]
    role = models.CharField(max_length=20, choices=roles, default='Utilisateur')
    telephone = models.CharField(max_length=20)
    
    class Meta :
        verbose_name = ("Utilisateur")
        verbose_name_plural = ("UTILISATEURS")
        ordering = ["username"]

    """@property
    def __str__(self):
        return f'{self.username}'"""

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_simple(self):
        return self.role == 'client'