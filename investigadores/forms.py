from django import forms
from .models import SolicitudTrabajo
from investigadores.models import Investigador, Investigacion
from usuarios.models import User


class FormInvestigador(forms.ModelForm):

    class Meta:
        model = Investigador
        exclude = ['latitud', 'longitud', 'aprobado']

    def __init__(self, *args, **kwargs):
        super(FormInvestigador, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(
            tipo_usuario__isnull=True)
        self.fields["user"].widget.attrs['class'] = 'form-select'
        self.fields["nivel"].widget.attrs['class'] = 'form-select'
        self.fields["curp"].widget.attrs['class'] = 'form-control'
        self.fields["curp"].widget.attrs['placeholder'] = 'Ingresa tu CURP'
        self.fields["codigo_postal"].widget.attrs['class'] = 'form-control'
        self.fields["codigo_postal"].widget.attrs['placeholder'] = (
            'Ingresa tu código postal de contacto')
        self.fields["municipio"].widget.attrs['class'] = 'form-select'
        self.fields["municipio"].widget.attrs['placeholder'] = (
            'Ingresa tu municipio de contacto')
        self.fields["colonia"].widget.attrs['class'] = 'form-control'
        self.fields["colonia"].widget.attrs['placeholder'] = (
            'Ingresa tu colonia de contacto')
        self.fields["calle"].widget.attrs['class'] = 'form-control'
        self.fields["calle"].widget.attrs['placeholder'] = (
            'Ingresa tu calle de contacto')
        self.fields["numero_exterior"].widget.attrs['class'] = 'form-control'
        self.fields["numero_exterior"].widget.attrs['placeholder'] = (
            'Ingresa tu número exterior de contacto')
        self.fields["acerca_de"].widget.attrs['class'] = 'form-control'
        self.fields["acerca_de"].widget.attrs['placeholder'] = (
            'Ingresa una breve descripción tuya')
        self.fields["imagen"].widget.attrs['class'] = 'form-control'


class FormInvestigadorUpdate(forms.ModelForm):

    class Meta:
        model = Investigador
        exclude = ['latitud', 'longitud', 'user', 'aprobado']

    def __init__(self, *args, **kwargs):
        super(FormInvestigadorUpdate, self).__init__(*args, **kwargs)
        self.fields["nivel"].widget.attrs['class'] = (
            'form-select')
        self.fields["curp"].widget.attrs['class'] = (
            'form-control')
        self.fields["curp"].widget.attrs['placeholder'] = (
            'Ingresa tu CURP')
        self.fields["codigo_postal"].widget.attrs['class'] = (
            'form-control')
        self.fields["codigo_postal"].widget.attrs['placeholder'] = (
            'Ingresa tu código postal de contacto')
        self.fields["municipio"].widget.attrs['class'] = (
            'form-select')
        self.fields["municipio"].widget.attrs['placeholder'] = (
            'Ingresa tu municipio de contacto')
        self.fields["colonia"].widget.attrs['class'] = (
            'form-control')
        self.fields["colonia"].widget.attrs['placeholder'] = (
            'Ingresa tu colonia de contacto')
        self.fields["calle"].widget.attrs['class'] = (
            'form-control')
        self.fields["calle"].widget.attrs['placeholder'] = (
            'Ingresa tu calle de contacto')
        self.fields["numero_exterior"].widget.attrs['class'] = (
            'form-control')
        self.fields["numero_exterior"].widget.attrs['placeholder'] = (
            'Ingresa tu número exterior de contacto')
        self.fields["acerca_de"].widget.attrs['class'] = (
            'form-control')
        self.fields["acerca_de"].widget.attrs['placeholder'] = (
            'Ingresa una breve descripción tuya')
        self.fields["imagen"].widget.attrs['class'] = (
            'form-control')


class FormInvestigadorBase(forms.ModelForm):

    class Meta:
        model = Investigador
        exclude = ['latitud', 'longitud', 'user', 'aprobado', 'nivel']

    def __init__(self, *args, **kwargs):
        super(FormInvestigadorBase, self).__init__(*args, **kwargs)
        self.fields["curp"].widget.attrs['class'] = (
            'form-control')
        self.fields["curp"].widget.attrs['placeholder'] = (
            'Ingresa tu CURP')
        self.fields["codigo_postal"].widget.attrs['class'] = (
            'form-control')
        self.fields["codigo_postal"].widget.attrs['placeholder'] = (
            'Ingresa tu código postal de contacto')
        self.fields["municipio"].widget.attrs['class'] = (
            'form-select')
        self.fields["municipio"].widget.attrs['placeholder'] = (
            'Ingresa tu municipio de contacto')
        self.fields["colonia"].widget.attrs['class'] = (
            'form-control')
        self.fields["colonia"].widget.attrs['placeholder'] = (
            'Ingresa tu colonia de contacto')
        self.fields["calle"].widget.attrs['class'] = (
            'form-control')
        self.fields["calle"].widget.attrs['placeholder'] = (
            'Ingresa tu calle de contacto')
        self.fields["numero_exterior"].widget.attrs['class'] = (
            'form-control')
        self.fields["numero_exterior"].widget.attrs['placeholder'] = (
            'Ingresa tu número exterior de contacto')
        self.fields["acerca_de"].widget.attrs['class'] = (
            'form-control')
        self.fields["acerca_de"].widget.attrs['placeholder'] = (
            'Ingresa una breve descripción tuya')
        self.fields["imagen"].widget.attrs['class'] = (
            'form-control')
        self.fields["link_google_scholar"].widget.attrs['class'] = (
            'form-control')
        self.fields["curriculum_vitae"].widget.attrs['class'] = (
            'form-control')


class FormInvestigacion(forms.ModelForm):
    class Meta:
        model = Investigacion
        fields = '__all__'

        widgets = {
            'titulo': forms.TextInput(
                attrs={'class': 'form-control'}),
            'categorias': forms.SelectMultiple(
                attrs={'class': 'form-select choices multiple-remove'}),
            'autores': forms.SelectMultiple(
                attrs={'class': 'form-select choices multiple-remove'}),
            'contenido': forms.Textarea(
                attrs={'class': 'form-control'}),
        }


class SolicitudTrabajoForm(forms.ModelForm):
    class Meta:
        model = SolicitudTrabajo
        fields = ('titulo', 'descripcion')
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-xl',
                    'placeholder': 'Título del trabajo'
                }),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-xl',
                    'placeholder': 'Decripción del trabajo'
                }),
        }
