from django import forms
from usuarios.models import User
from instituciones_educativas.models import InstitucionEducativa


class FormInstitucionEducativa(forms.ModelForm):

    class Meta:
        model = InstitucionEducativa
        exclude = ['latitud', 'longitud', 'aprobado']

    def __init__(self, *args, **kwargs):
        super(FormInstitucionEducativa, self).__init__(*args, **kwargs)
        self.fields["encargado"].queryset = User.objects.filter(
            tipo_usuario__isnull=True)
        self.fields["encargado"].widget.attrs['class'] = (
            'form-select')
        self.fields["nombre_institucion"].widget.attrs['class'] = (
            'form-control')
        self.fields["especialidades"].widget.attrs['class'] = (
            'form-select choices multiple-remove')
        self.fields["miembros"].widget.attrs['class'] = (
            'form-select choices multiple-remove')
        self.fields["codigo_postal"].widget.attrs['class'] = (
            'form-control')
        self.fields["codigo_postal"].widget.attrs['placeholder'] = (
            'Ingresa tu código de contacto')
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
            'Ingresa una breve descripción de la institución educativa')
        self.fields["imagen"].widget.attrs['class'] = (
            'form-control')


class FormInstitucionEducativaUpdate(forms.ModelForm):

    class Meta:
        model = InstitucionEducativa
        exclude = ['latitud', 'longitud', 'encargado', 'aprobado']

    def __init__(self, *args, **kwargs):
        super(FormInstitucionEducativaUpdate, self).__init__(*args, **kwargs)
        self.fields["nombre_institucion"].widget.attrs['class'] = (
            'form-control')
        self.fields["especialidades"].widget.attrs['class'] = (
            'form-select choices multiple-remove')
        self.fields["miembros"].widget.attrs['class'] = (
            'form-select choices multiple-remove')
        self.fields["codigo_postal"].widget.attrs['class'] = (
            'form-control')
        self.fields["codigo_postal"].widget.attrs['placeholder'] = (
            'Ingresa tu código de contacto')
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
            'Ingresa una breve descripción de la institución educativa')
        self.fields["imagen"].widget.attrs['class'] = (
            'form-control')
