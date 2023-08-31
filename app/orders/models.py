from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
