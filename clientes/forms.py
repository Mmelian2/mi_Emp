from django import forms
from .models import cliente, contacto, empresa


class FormCliente(forms.ModelForm):
    class Meta:
        model=cliente
        fields='__all__'
        
class FormEmpresa(forms.ModelForm):
    class Meta:
        model=empresa
        fields='__all__'

class ContactoForm(forms.ModelForm):
    class Meta:
        model = contacto
        fields ='__all__'
        widgets = {'email': forms.EmailInput(attrs={'type':'email'}),
        }