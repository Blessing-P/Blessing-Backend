# apps/catalog/urls.py

from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    UnitListCreateView,
    UnitDetailView,
)

urlpatterns = [
    path('categories/',          CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('units/',               UnitListCreateView.as_view()),
    path('units/<int:pk>/',      UnitDetailView.as_view()),
]