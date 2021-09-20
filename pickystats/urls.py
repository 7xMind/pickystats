from django.urls import path

from .api import views

urlpatterns = [
    path('', views.DataAnalyzerView.as_view())
]
