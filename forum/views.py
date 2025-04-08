from django.shortcuts import render
from forum.models import Ticket
from django.views.generic import ListView
# Create your views here.

class TicketsListView(ListView):
    model = Ticket
    context_object_name = "tickets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    