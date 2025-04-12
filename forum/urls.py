from django.urls import path
from forum import views
urlpatterns = [
    path("", views.TicketsListView.as_view(), name="ticket-list"),
    path("<int:pk>", views.TicketDetails , name="ticket-details"),
    path("create-ticket", views.CreateTicket.as_view(), name="ticket-create"),
]