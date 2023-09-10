from django import forms
from .models import SolicitudTrabajo
from investigadores.models import Investigador, Investigacion, CategoriaA, CategoriaB, RevisoresCatA, RevisoresCatB
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
        super(FormCategoriaB, self).__init__(*args, **kwargs)
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

class FormRevisorCatA(forms.ModelForm):
    class Meta:
        model = RevisoresCatA
        exclude = ["downloadZipFile", 'revisor', 'solicitud', 'estatus']

        CHOICES = [
            (['1', '1']),
            (['2', '2']),
            (['3', '3']),
            (['4', '4']),
            (['5', '5']),
            (['6', '6']),
            (['7', '7']),
            (['8', '8']),
            (['9', '9']),
            (['10', '10']),
        ]

        widgets = {
            'a1': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a1_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a2': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a2_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a3': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a3_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a4': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a4_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a5': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a5_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a6': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a6_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a7': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a7_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a8': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a8_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a9': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a9_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'a10': forms.RadioSelect(choices=CHOICES, attrs={'style': 'display: inline;'}),
            'a10_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
        }

class FormRevisorCatB(forms.ModelForm):
    class Meta:
        model = RevisoresCatB
        exclude = ["downloadZipFile", 'revisor', 'solicitud', 'estatus']

        CHOICES1 = [
            (['1', '1']),
            (['2', '2']),
            (['3', '3']),
            (['4', '4']),
            (['5', '5']),
            (['6', '6']),
            (['7', '7']),
            (['8', '8']),
            (['9', '9']),
            (['10', '10']),
        ]
        CHOICES2 = [
            (['1', '1']),
            (['2', '2']),
            (['3', '3']),
            (['4', '4']),
            (['5', '5']),
            (['6', '6']),
            (['7', '7']),
            (['8', '8']),
            (['9', '9']),
            (['10', '10']),
            (['11', '11']),
            (['12', '12']),
            (['13', '13']),
            (['14', '14']),
            (['15', '15']),
        ]
        CHOICES3 = [
            (['1', '1']),
            (['2', '2']),
            (['3', '3']),
            (['4', '4']),
            (['5', '5']),
        ]

        widgets = {
            'b1': forms.RadioSelect(choices=CHOICES2, attrs={'style': 'display: inline;'}),
            'b1_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b2': forms.RadioSelect(choices=CHOICES3, attrs={'style': 'display: inline;'}),
            'b2_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b3': forms.RadioSelect(choices=CHOICES1, attrs={'style': 'display: inline;'}),
            'b3_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b4': forms.RadioSelect(choices=CHOICES1, attrs={'style': 'display: inline;'}),
            'b4_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b5': forms.RadioSelect(choices=CHOICES1, attrs={'style': 'display: inline;'}),
            'b5_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b6': forms.RadioSelect(choices=CHOICES2, attrs={'style': 'display: inline;'}),
            'b6_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b7': forms.RadioSelect(choices=CHOICES1, attrs={'style': 'display: inline;'}),
            'b7_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b8': forms.RadioSelect(choices=CHOICES1, attrs={'style': 'display: inline;'}),
            'b8_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b9': forms.RadioSelect(choices=CHOICES3, attrs={'style': 'display: inline;'}),
            'b9_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
            'b10': forms.RadioSelect(choices=CHOICES1, attrs={'style': 'display: inline;'}),
            'b10_comentario': forms.Textarea(attrs={ 'class': 'form-control'}),
        }