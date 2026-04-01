from .models import OrderReview, CustomUser, Order
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Parašykite savo atsiliepimą čia...',
            })
        }
        labels = {
            'content': 'Atsiliepimo tekstas',
        }

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Vardas',
            'last_name': 'Pavardė',
            'email': 'El. paštas',
            'photo': 'Profilio nuotrauka',
        }

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'due_back']
        widgets = {'due_back': forms.DateInput(attrs={'type':'date',
                                                      'class':'form-control',})}
        labels = {
            'car': 'Automobilis',
            'due_back': 'Terminas (iki kada)',
        }

