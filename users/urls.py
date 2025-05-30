from django.urls import path
from .views import LoginView, RegistrationView

urlpatterns = [  
    path('register/', RegistrationView.as_view(), name="register"),
    path('', LoginView.as_view(), name="login"),
]