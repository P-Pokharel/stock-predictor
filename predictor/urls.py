from django.urls import path
from .views import HomeView, PredictionView

urlpatterns = [
    
    path('', HomeView.as_view(), name='home'),
    path('predict/', PredictionView.as_view(), name='prediction'),
]