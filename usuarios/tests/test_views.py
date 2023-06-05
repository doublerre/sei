from django.test import TestCase
from usuarios.models import User


class TestRegistroUsuario(TestCase):

    def test_registro_correcto(self):
        self.client.post("/usuarios/registrar", {
            "username": "elias",
            "password": "12345678",
            "email": "elias@redacted.com",
            "repassword": "12345678"
        })

        self.assertEquals(User.objects.count(), 1)
