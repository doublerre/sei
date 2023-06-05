from django.test import TestCase
from usuarios.models import User


class TestViewEmpresas(TestCase):

    def test_lista_empresas_estatus(self):
        usuario = User.objects.create(
            username="unittest",
            email="unit@test.com")
        usuario.set_password("password")
        usuario.save()
        self.client.login(username="unittest", password="password")
        resupesta = self.client.get("/empresas")
        self.assertEquals(resupesta.status_code, 200)
