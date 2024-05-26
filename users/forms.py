from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    personal_number = forms.CharField(max_length=20, required=True)
    birth_date = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'personal_number', 'birth_date', 'password1',
                  'password2', 'first_name', 'last_name')
