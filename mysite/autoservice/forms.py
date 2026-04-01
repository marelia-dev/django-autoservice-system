from .models import OrderReview, CustomUser, Order, OrderLine, Service
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory



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
        widgets = {
            'due_back': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'car': 'Automobilis',
            'due_back': 'Terminas (data)',
        }
        input_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y']


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'due_back', 'status']
        widgets = {
            'due_back': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
                format='%Y-%m-%d'
            ),
        }
        input_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y']

class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['service', 'quantity']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }
        labels = {
            'service': 'Paslauga',
            'quantity': 'Kiekis',
        }


OrderLineFormSet = inlineformset_factory(
    Order,
    OrderLine,
    form=OrderLineForm,
    extra=1,
    can_delete=True,
    min_num=0,
    max_num=20,
    absolute_max=20,
    validate_min=False,
)