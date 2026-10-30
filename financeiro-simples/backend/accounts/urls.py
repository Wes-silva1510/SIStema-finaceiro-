from django.urls import path

from . import views

urlpatterns = [
    path("accounts/", views.AccountListCreate.as_view()),
    path("accounts/<int:pk>/transactions/", views.AccountTransactions.as_view()),
    path("transfers/", views.TransferView.as_view()),
]
