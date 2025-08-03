from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from .models import Category
from .models import ContactMessage
from .models import Order



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price','category', 'image','stock',  'badge']

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Sélectionner une catégorie",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']






class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']




class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('orange_money', 'Orange Money'),
        ('card', 'Carte bancaire'),
        ('cash_on_delivery', 'Espèces à la livraison'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment_method']
