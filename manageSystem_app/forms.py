from django import forms
from .models import Order, OrderDish, Dish, Table

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class OrderForm(forms.ModelForm):
    dish = forms.ModelChoiceField(queryset=Dish.objects.all(), label='Dish')
    quantity = forms.IntegerField(min_value=1)
    table = forms.ModelChoiceField(queryset=Table.objects.all(), label='Table')

    class Meta:
        model = Order
        fields = ['table', 'dish', 'quantity']
