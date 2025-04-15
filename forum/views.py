from django.shortcuts import render , get_object_or_404 , redirect , HttpResponseRedirect
from forum.models import Ticket , Comment , CommentLike
from forum.forms import TicketForm , CommentForm
from django.views.generic import ListView , CreateView , DetailView
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
    ticket = Ticket.objects.get(id=pk)
    context = {
        'ticket' : ticket,
        'comment_form': CommentForm
    }

    return render(request, "forum/ticket_detail.html", context)

def CommentCreate(request, pk):  
    ticket = Ticket.objects.get(id=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.ticket = ticket
            comment.save()
            return redirect("ticket-details", pk=ticket.pk)
    else:
        comment_form = CommentForm()
    
def CommentLikeAdd(request, pk):
    if request.method == "POST":
        comment = Comment.objects.get(id=pk)
        liked = CommentLike.objects.filter(comment=comment, creator=request.user)
        if liked.exists():
            liked.delete()
        else:
            CommentLike.objects.create(comment=comment, creator=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())