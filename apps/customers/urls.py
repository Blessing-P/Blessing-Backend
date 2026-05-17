# customers/urls.py

from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path('',     CustomerListCreateView.as_view()),   # GET, POST
    path('<int:pk>/', CustomerDetailView.as_view()),  # GET, PUT, DELETE
]