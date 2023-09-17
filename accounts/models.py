from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    UNIT_CHOICES = (
        ('ml', _('Milliliters')),
        ('oz', _('Ounces')),
        # Add more choices as needed
    )
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='ml')

