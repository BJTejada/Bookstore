from django import forms
from .models import VENTAS, DETALLEVENTAS

class VentaForm(forms.ModelForm):
    class Meta:
        model = VENTAS
        fields = []

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DETALLEVENTAS
        fields = []


class ClienteForm(forms.Form):
    nombres = forms.CharField(max_length=50, required=True)
    apellidos = forms.CharField(max_length=50, required=True)
    telefono = forms.CharField(max_length=15, required=True)
    dui = forms.CharField(max_length=10, required=True)
    correo = forms.EmailField(required=True)
