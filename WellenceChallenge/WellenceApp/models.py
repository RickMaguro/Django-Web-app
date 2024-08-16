from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Accounts(models.Model):
    password = models.CharField(max_length=255)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

class Tasks(models.Model):
    MY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    userEmail = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    due_by = models.DateTimeField()
    priority = models.IntegerField(choices=MY_CHOICES, default=1)
    is_urgent = models.BooleanField(default=False)

