from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product,Category,Order

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

class LoginForm(forms.Form):
    email = forms.EmailField(required = True)
    password = forms.CharField()

class ProductAddForm(forms.ModelForm):
    category = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. Shoes, Clothing, Electronics",
        })
    )
    class Meta:
        model = Product
        fields = ['name','slug','price','stock','image','description','is_available']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =['full_name','phone','city','address','payment']