from django.test import TestCase
from usuarios.models import User
from usuarios.forms import UserForm


class TestUsuarioForm(TestCase):
    def setUp(self):
        self.form = UserForm({
            "username": "elias",
            "password": "12345678",
            "email": "elias@redacted.com",
            "repassword": "12345678"
        })

    def test_formulario_correcto(self):
        if self.form.is_valid():
            self.form.save()
        else:
            pass
        self.assertEquals(User.objects.count(), 1)

    def test_nombre_requerido(self):
        del self.form.data["username"]
        self.assertFalse(self.form.is_valid())

    def test_password_requerido(self):
        del self.form.data["password"]
        self.assertFalse(self.form.is_valid())

    def test_password_min_size(self):
        self.form.data["password"] = "a"*7
        self.assertFalse(self.form.is_valid())

    def test_nombre_caracteres_especiales(self):
        self.form.data["username"] = "Nombre invalido\n"
        self.assertFalse(self.form.is_valid())

    def test_email_requerido(self):
        del self.form.data["email"]
        self.assertFalse(self.form.is_valid())

    def test_email_formato(self):
        self.form.data["email"] = "formatonovalido.com"
        self.assertFalse(self.form.is_valid())
