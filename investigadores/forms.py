from django import forms
from .models import SolicitudTrabajo
from investigadores.models import Investigador, Investigacion, CategoriaA, CategoriaB
from usuarios.models import User


class FormInvestigador(forms.ModelForm):

    class Meta:
        model = Investigador
        exclude = ['latitud', 'longitud', 'aprobado', 'es_sei', 'es_sni', 'constancia']

    def __init__(self, *args, **kwargs):
        super(FormInvestigador, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(
            tipo_usuario__isnull=True)
        self.fields["nombre_completo"].widget.attrs['class'] = 'form-control'
        self.fields["nombre_completo"].widget.attrs['placeholder'] = ('Escribe tu nombre')
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
        self.fields["grado"].widget.attrs['class'] = (
            'form-control')


class FormInvestigadorUpdate(forms.ModelForm):

    class Meta:
        model = Investigador
        exclude = ['latitud', 'longitud', 'user', 'aprobado', 'constancia']

    def __init__(self, *args, **kwargs):
        super(FormInvestigadorUpdate, self).__init__(*args, **kwargs)
        self.fields["nombre_completo"].widget.attrs['class'] = 'form-control'
        self.fields["nombre_completo"].widget.attrs['placeholder'] = ('Escribe tu nombre')
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
        self.fields["curriculum_vitae"].widget.attrs['class'] = (
            'form-control')
        self.fields["grado"].widget.attrs['class'] = (
            'form-control')


class FormInvestigadorBase(forms.ModelForm):

    class Meta:
        model = Investigador
        exclude = ['latitud', 'longitud', 'user', 'aprobado', 'nivel', 'es_sei', 'es_sni', 'constancia']

    def __init__(self, *args, **kwargs):
        super(FormInvestigadorBase, self).__init__(*args, **kwargs)
        self.fields["nombre_completo"].widget.attrs['class'] = 'form-control'
        self.fields["nombre_completo"].widget.attrs['placeholder'] = ('Escribe tu nombre')
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
        self.fields["grado"].widget.attrs['class'] = (
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

class FormCategoriaA(forms.ModelForm):
    class Meta:
        model = CategoriaA
        exclude = ["estatus", "user", "anio"]
    def __init__(self, *args, **kwargs):
        super(FormCategoriaA, self).__init__(*args, **kwargs)
        self.fields["a1"].widget.attrs['class'] = 'form-control'
        self.fields["a2"].widget.attrs['class'] = 'form-control'
        self.fields["a3"].widget.attrs['class'] = 'form-control'
        self.fields["a4"].widget.attrs['class'] = 'form-control'
        self.fields["a5"].widget.attrs['class'] = 'form-control'
        self.fields["a6"].widget.attrs['class'] = 'form-control'
        self.fields["a7"].widget.attrs['class'] = 'form-control'
        self.fields["a8"].widget.attrs['class'] = 'form-control'
        self.fields["a9"].widget.attrs['class'] = 'form-control'
        self.fields["a10"].widget.attrs['class'] = 'form-control'

class FormCategoriaB(forms.ModelForm):
    class Meta:
        model = CategoriaB
        exclude = ["estatus", "user", "anio"]
    def __init__(self, *args, **kwargs):
        super(FormCategoriaA, self).__init__(*args, **kwargs)
        self.fields["b1"].widget.attrs['class'] = 'form-control'
        self.fields["b2"].widget.attrs['class'] = 'form-control'
        self.fields["b3"].widget.attrs['class'] = 'form-control'
        self.fields["b4"].widget.attrs['class'] = 'form-control'
        self.fields["b5"].widget.attrs['class'] = 'form-control'
        self.fields["b6"].widget.attrs['class'] = 'form-control'
        self.fields["b7"].widget.attrs['class'] = 'form-control'
        self.fields["b8"].widget.attrs['class'] = 'form-control'
        self.fields["b9"].widget.attrs['class'] = 'form-control'
        self.fields["b10"].widget.attrs['class'] = 'form-control'

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
