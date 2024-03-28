from django import forms
from django.db.models import fields
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    nombre = forms.CharField(max_length=20, min_length=4)
    apellido = forms.CharField(max_length=20, min_length=4)
    direccion = forms.CharField(max_length=40)
    telefono = forms.IntegerField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['nombre','apellido','direccion','telefono','username', 'email', 'password1', 'password2']

""" 
    PRODUCTO 
"""
class FormProducto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('titulo','imagen','descripcion','precio','categoria','stock')
        """ widgets = {
            'titulo': forms.TextInput(),
            'descripcion' : forms.Textarea(),
            'precio' : forms.NumberInput(),
            'stock': forms.NumberInput(),
            'imagen' : forms.FileField()
        } """
        """ widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Ingrese el nombre del producto...' , 'required': True}),
            'descripcion' : forms.Textarea(attrs={'class' : 'form-control', 'row' : 3, 'required': True}),
            'precio' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'XXXX.XX', 'required': True}),
            'stock' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'XXXX.XX', 'required': True}),
            'imagen' : forms.FileField(attrs={'class':'form-control-file', 'id':'imagen', 'placeholder': 'Ingrese la imagen...', 'required': True})
        } """

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=20)
    apellido = forms.CharField(max_length=20)
    telefono = forms.IntegerField()
    email = forms.EmailField()
    servicio = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)