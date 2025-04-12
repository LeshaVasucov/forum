from django.shortcuts import render , get_object_or_404 
from forum.models import Ticket
from forum.forms import TicketForm
from django.views.generic import ListView , CreateView
from django.urls import reverse_lazy
# Create your views here.

class TicketsListView(ListView):
    model = Ticket
    context_object_name = "tickets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateTicket(CreateView):
    model = Ticket
    success_url = reverse_lazy("ticket-list")
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


def TicketDetails(request, pk):
    ticket = Ticket.objects.get( id=pk)
    context = {
        'ticket' : ticket,
    }
    return render(request, "forum/ticket_detail.html", context)
    