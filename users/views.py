from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm()
        context = {'form': form}
        return render(request, "users/registration.html", context)
    
    def post(self, request):
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        return render(request, "users/registration.html", {'form': form})


class LoginView(View):
    
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, "users/login.html", context)
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'users/login.html', {'form': form})

