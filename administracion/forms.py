from django import forms
from administracion.models import Contacto, AcercaDe, Premios
from usuarios.models import User
from vinculacion.models import Categoria, Noticia
import datetime


class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'es_revisor']

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(FormUser, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}),
            'area_conocimiento': forms.Select(
                attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control'}),
        }


class FormNoticia(forms.ModelForm):
    class Meta:
        model = Noticia
        exclude = ['fecha']

        widgets = {
            'titulo': forms.TextInput(
                attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(
                attrs={'class': 'form-control'}),
            'escritor': forms.Select(
                attrs={'class': 'form-select'}),
        }


class FormContacto(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = "__all__"

        widgets = {
            'datos': forms.Textarea(
                attrs={'class': 'form-control'}
            )
        }


class FormAcercaDe(forms.ModelForm):
    class Meta:
        model = AcercaDe
        fields = "__all__"

        widgets = {
            'datos': forms.Textarea(
                attrs={'class': 'form-control'}
            )
        }

class FormPremios(forms.ModelForm):
    class Meta:
        model = Premios
        fields = "__all__"

        widgets = {
            'fecha_inicio': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'type': 'date',
                    'min': datetime.date.today()
                },
            ),
            'fecha_fin': forms.widgets.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                },
            ),
        }