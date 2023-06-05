from django.test import TestCase
from django.core.exceptions import ValidationError
from usuarios.models import User, TipoUsuario


class TestUsuario(TestCase):
    def setUp(self):
        self.tipo = TipoUsuario.objects.create(
            tipo="Investigador")
        self.usuario = User.objects.create(
            username="Prueba",
            email="asd@asd.com",
            is_active=True,
            tipo_usuario=self.tipo,
            aprobado=True)

    def test_to_string(self):
        self.assertEquals(str(self.usuario), "Prueba")

    def test_nombre_requerido(self):
        self.usuario.username = ""
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_password_requerido(self):
        self.usuario.password = ""
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_password_min_size(self):
        self.usuario.password = "a"*7
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_nombre_min_size(self):
        self.usuario.username = "a"*2
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_nombre_max_size(self):
        self.usuario.username = "a"*31
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_nombre_caracteres_especiales(self):
        self.usuario.username = "Nombre invalido\n"
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_email_requerido(self):
        self.usuario.email = ""
        self.assertRaises(ValidationError, self.usuario.full_clean)

    def test_email_formato(self):
        self.usuario.email = "formatonovalido.com"
        self.assertRaises(ValidationError, self.usuario.full_clean)
