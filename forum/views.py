from django.shortcuts import render , redirect , HttpResponseRedirect
from forum.models import Ticket , Comment , CommentLike , Profile
from forum.forms import TicketForm , CommentForm
from django.views.generic import ListView , CreateView 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Aianswers.views import AiAnswerCreate
from Aianswers.models import AiAnswer
class TicketsListView(ListView):
    model = Ticket
    context_object_name = "tickets"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CreateTicket(LoginRequiredMixin, CreateView):
    model = Ticket
    success_url = reverse_lazy("ticket-list")
    form_class = TicketForm

    def form_valid(self, form):
        form.instance.creator = self.request.user

        profile = self.request.user.profile 
        response = super().form_valid(form)
        ticket = form.save()
        print(profile , ticket)
        profile.tickets.add(ticket)  
        profile.save()
        AiAnswerCreate(pk=ticket.pk)

        return response
@login_required 
def TicketDetails(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ai_answer = AiAnswer.objects.get(id=pk)
    comments = ticket.comments.all()
    for comment in comments:
        comment.is_liked_by_user = comment.likes.filter(creator=request.user).exists()

    context = {
        'ticket' : ticket,
        'comments': comments, 
        'comment_form': CommentForm,
        'aianswer' : ai_answer.text,
    }

    return render(request, "forum/ticket_detail.html", context)
@login_required
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
@login_required
def CommentLikeAdd(request, pk):
    if request.method == "POST":
        comment = Comment.objects.get(id=pk)
        liked = CommentLike.objects.filter(comment=comment, creator=request.user)
        if liked.exists():
            liked.delete()
        else:
            CommentLike.objects.create(comment=comment, creator=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())
    

def ProfileView(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {
        "profile" : profile
    }

    return render(request, "forum/profile.html", context)