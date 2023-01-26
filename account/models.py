import datetime
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid_until = models.DateField(
        default=datetime.date.today()
    )
    phone_number = models.CharField(max_length=15, null=True)

    def has_paid(self):
        current_date = datetime.date.today()

        return current_date < self.paid_until

    def __str__(self):
        return self.user.username