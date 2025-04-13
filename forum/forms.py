from forum.models import Ticket , Comment
from django import forms
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "status"]

        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]