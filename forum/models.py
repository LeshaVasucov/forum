from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ticket(models.Model):
    STATUS_CHOICES = [
        ("opened", "Відкритий"),
        ("closed", "Закритий"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES, default="opened")
    creator = models.ForeignKey(User ,on_delete=models.DO_NOTHING, blank=True, related_name="tickets")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title