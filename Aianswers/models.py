from django.db import models
from forum.models import Ticket
# Create your models here.

class AiAnswer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.ticket
