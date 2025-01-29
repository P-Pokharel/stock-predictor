from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "firstName",
                                        'placeholder': "First Name"
                                    }
                                )
                            )
    
    last_name = forms.CharField(widget=forms.TextInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "lastName",
                                        'placeholder': "Last Name"
                                    }
                                )
                            )
    
    username = forms.CharField(widget=forms.TextInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "username",
                                        'placeholder': "Username"
                                    }
                                )
                            )
    
    email = forms.EmailField(widget=forms.TextInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "email",
                                        'placeholder': "Email"
                                    }
                                )
                            )
    
    password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "password1",
                                        'placeholder': "Password"
                                    }
                                )
                            )
    
    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "password2",
                                        'placeholder': "Confirm Password"
                                    }
                                )
                            )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "username",
                                        'placeholder': "Enter your username",
                                    }
                                )
                            )
    
    password = forms.CharField(required=True, widget=forms.PasswordInput(
                                    attrs={
                                        'class': "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                                        'id': "password",
                                        'placeholder': "Enter your password",
                                    }
                                )
                            )
    
    class Meta:
        model = User
        fields = ['username', 'password']
