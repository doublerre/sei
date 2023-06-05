from django import forms
from usuarios.models import User
from empresas.models import Empresa


class FormEmpresa(forms.ModelForm):

    class Meta:
        model = Empresa
        exclude = ['latitud', 'longitud', 'aprobado']

    def __init__(self, *args, **kwargs):
        super(FormEmpresa, self).__init__(*args, **kwargs)
        self.fields["encargado"].queryset = User.objects.filter(
            tipo_usuario__isnull=True)
        self.fields["encargado"].widget.attrs['class'] = (
            'form-select')
        self.fields["nombre_empresa"].widget.attrs['class'] = (
            'form-control')
        self.fields["especialidades"].widget.attrs['class'] = (
            'form-select choices multiple-remove')
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
            'Ingresa una breve descripción de la empresa')
        self.fields["imagen"].widget.attrs['class'] = (
            'form-control')


class FormEmpresaUpdate(forms.ModelForm):

    class Meta:
        model = Empresa
        exclude = ['latitud', 'longitud', 'encargado', 'aprobado']

    def __init__(self, *args, **kwargs):
        super(FormEmpresaUpdate, self).__init__(*args, **kwargs)
        self.fields["nombre_empresa"].widget.attrs['class'] = (
            'form-control')
        self.fields["especialidades"].widget.attrs['class'] = (
            'form-select choices multiple-remove')
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
            'Ingresa una breve descripción de la empresa')
        self.fields["imagen"].widget.attrs['class'] = (
            'form-control')
