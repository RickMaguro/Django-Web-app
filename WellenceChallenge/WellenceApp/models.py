from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Accounts(models.Model):
    password = models.CharField(max_length=255)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

class Tasks(models.Model):
    id = models.IntegerField(primary_key=True)
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    email = models.EmailField()
    task = models.CharField(max_length=255)
    due_by = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    is_urgent = models.BooleanField(default=False)





