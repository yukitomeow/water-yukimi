from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext as _


class WaterConsumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_drank = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"User: {self.user}, {_('Amount Drank')}: {self.amount_drank}, Date: {self.date}"

        
   