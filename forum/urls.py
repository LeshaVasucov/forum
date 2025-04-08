from django.urls import path
from forum import views
urlpatterns = [
    path("", views.TicketsListView.as_view(),name="ticket-list"),
]