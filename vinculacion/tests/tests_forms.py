from investigadores.forms import SolicitudTrabajoForm
from django.test import TestCase


class TestSolicitudTrabajoForm(TestCase):

    def test_form_valido(self):
        form = SolicitudTrabajoForm({
            "titulo": "Titulo valido",
            "descripcion": "Descripcion valida"
        })
        self.assertTrue(form.is_valid())

    def test_form_vacio(self):
        form = SolicitudTrabajoForm({
        })
        self.assertFalse(form.is_valid())

    def test_form_no_titulo(self):
        form = SolicitudTrabajoForm({
            "descripcion": "Descripcion valida"
        })
        self.assertFalse(form.is_valid())

    def test_form_no_titulo_error(self):
        form = SolicitudTrabajoForm({
            "descripcion": "Descripcion valida"
        })
        self.assertEquals(
            form.errors["titulo"],
            ['Este campo es obligatorio.'])

    def test_form_titulo_vacio(self):
        form = SolicitudTrabajoForm({
            "titulo": "",
            "descripcion": "Descripcion valida"
        })
        self.assertFalse(form.is_valid())

    def test_form_titulo_largo(self):
        form = SolicitudTrabajoForm({
            "titulo": "a"*250,
            "descripcion": "Descripcion valida"
        })
        if form.is_valid():
            self.assertEquals(len(form.cleaned_data["titulo"]), 200)

    def test_form_no_descripcion(self):
        form = SolicitudTrabajoForm({
            "titulo": "Titulo valido",
        })
        self.assertFalse(form.is_valid())

    def test_form_no_descripcion_error(self):
        form = SolicitudTrabajoForm({
            "titulo": "Titulo valido",
        })
        self.assertEquals(
            form.errors["descripcion"],
            ['Este campo es obligatorio.'])

    def test_form_descripcion_vacio(self):
        form = SolicitudTrabajoForm({
            "titulo": "Titulo valido",
            "descripcion": ""
        })
        self.assertFalse(form.is_valid())

    def test_form_descripcion_largo(self):
        form = SolicitudTrabajoForm({
            "titulo": "Titulo valido",
            "descripcion": "a"*5001
        })
        if form.is_valid():
            self.assertEquals(len(form.cleaned_data["titulo"]), 5000)
