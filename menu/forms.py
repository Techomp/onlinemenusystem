from django import forms
from .models import Menu, Category, Product

# class MenuForm(forms.ModelForm):
#     name = forms.CharField(widget=forms.TextInput(attrs={
#         "class": "className",
#         "placeholder": "Name"
#     }))
#     image = forms.ImageField()
#     class Meta:
#         model = Menu
#         fiels = ["name, image"]