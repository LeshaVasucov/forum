from django.db import models
from django.urls import reverse
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
    creator = models.ForeignKey(User ,on_delete=models.DO_NOTHING, blank=True, related_name="ticket")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ticket-details', kwargs={'pk': self.pk})
    

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return self.ticket.get_absolute_url()
    
class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'creator')
