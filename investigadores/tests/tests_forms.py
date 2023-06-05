from django.test import TestCase
from investigadores.forms import FormInvestigador, FormInvestigadorBase
from usuarios.models import User
from investigadores.models import NivelInvestigador


class TestInvestigadorForm(TestCase):
    def setUp(self):
        self.nivel = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="XD"
        )
        self.usuario = User.objects.create_user(
            username='testuser', password='12345678', email="test@mail.com")
        self.usuario.set_password("12345678")
        self.usuario.save()
        self.form = FormInvestigador({
            "acerca_de": "a",
            "calle": "Esmeralda",
            "codigo_postal": 98613,
            "colonia": "Las Joyas",
            "curp": "BEGE010204HZSLNLA5",
            "municipio": 16,
            "numero_exterior": 35,
            "user": self.usuario.pk,
            "nivel": self.nivel.pk,
        })

    def test_formulario_correcto(self):
        formulario = FormInvestigadorBase({
            "acerca_de": "a",
            "calle": "Esmeralda",
            "codigo_postal": 98613,
            "colonia": "Las Joyas",
            "curp": "BEGE010204HZSLNLA5",
            "municipio": 16,
            "numero_exterior": 35,
        })

        self.assertTrue(formulario.is_valid())

    def test_usuario_requerido(self):
        del self.form.data["user"]
        self.assertFalse(self.form.is_valid())

    def test_curp_requerido(self):
        del self.form.data["curp"]
        self.assertFalse(self.form.is_valid())

    def test_curp_formato(self):
        self.form.data["curp"] = "BEGEZZZ"
        self.assertFalse(self.form.is_valid())

    def test_calle_requerido(self):
        del self.form.data["calle"]
        self.assertFalse(self.form.is_valid())

    def test_descripcion_requerida(self):
        del self.form.data["acerca_de"]
        self.assertFalse(self.form.is_valid())

    def test_codigo_postal_requerido(self):
        del self.form.data["codigo_postal"]
        self.assertFalse(self.form.is_valid())

    def test_codigo_postal_formato(self):
        self.form.data["curp"] = 31
        self.assertFalse(self.form.is_valid())

    def test_colonia_requerido(self):
        del self.form.data["colonia"]
        self.assertFalse(self.form.is_valid())

    def test_municipio_requerido(self):
        del self.form.data["municipio"]
        self.assertFalse(self.form.is_valid())

    def test_numero_exterior_requerido(self):
        del self.form.data["numero_exterior"]
        self.assertFalse(self.form.is_valid())

    def test_nivel_requerido(self):
        del self.form.data["nivel"]
        self.assertFalse(self.form.is_valid())
