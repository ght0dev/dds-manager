from django.urls import path
from . import views

app_name = "transactions"

urlpatterns = [
    path("", views.index, name="index"),
    path("transactions/new/", views.transaction_create, name="transaction_create"),
    path("transactions/<int:pk>/edit/", views.transaction_edit, name="transaction_edit"),
]
