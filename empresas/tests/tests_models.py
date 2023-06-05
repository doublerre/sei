from django.test import TestCase
from django.core.exceptions import ValidationError
from empresas.models import Empresa
from usuarios.models import User, TipoUsuario
from helpers.empresas_helpers import crear_empresa
from helpers.vinculacion_helpers import (
    crear_area_conocimiento, crear_categoria)
from helpers.usuarios_helpers import crear_tipo_usuario, crear_usuario


# Create your tests here.
class TestEmpresa(TestCase):

    def setUp(self):
        self.tipo_empresa = TipoUsuario.objects.create(tipo="Empresa")
        self.usuario = User.objects.create(
            password="test",
            username="Pruebita",
            email="asd@asd.com",
            is_active=True,
            tipo_usuario=self.tipo_empresa,
            aprobado=True)

    def test_insertar_empresa_contenido(self):
        Empresa.objects.create(
            encargado=self.usuario,
            nombre_empresa="Oxxo",
            latitud=5,
            longitud=5,
            municipio=1,
            colonia="a",
            calle="a",
            numero_exterior=32,
            acerca_de="a")

        self.assertEquals(Empresa.objects.count(), 1)

    def test_insertar_empresa_nombre(self):
        empresa = Empresa.objects.create(
            encargado=self.usuario,
            nombre_empresa="Oxxo",
            latitud=5,
            longitud=5,
            municipio=1,
            colonia="a",
            calle="a",
            numero_exterior=32,
            acerca_de="a")

        empresa2 = Empresa.objects.get(nombre_empresa='Oxxo')

        self.assertEquals(empresa.nombre_empresa, empresa2.nombre_empresa)

    def test_insertar_empresa_validacion(self):
        empresa = Empresa.objects.create(
            encargado=self.usuario,
            nombre_empresa="Oxxo",
            latitud=5,
            longitud=5,
            municipio=1,
            colonia="a",
            calle="a",
            numero_exterior=32,
            acerca_de="a")

        empresa.nombre_empresa = "A"*500
        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_nombre_empresa_str(self):
        area_conocimiento = crear_area_conocimiento(
            "Ingeniería",
            "Sobre ingeniería")
        categoria = crear_categoria(
            "Software", area_conocimiento, "Sobre software")
        tipo_empresa = crear_tipo_usuario("Empresa")
        usuario_encargado = crear_usuario(
            usuario="encargado",
            correo="encargado@encargado.com",
            contra="12345678",
            tipo=tipo_empresa,
            aprobado=True
        )
        self.empresa = crear_empresa(
            encargado=usuario_encargado,
            nombre_empresa="Empresa",
            codigo_postal='99390',
            municipio=19,
            especialidades=[categoria],
            colonia='Alamitos',
            calle='Mezquite',
            numero_exterior='29',
            acerca_de='Info',
            imagen="/tmp/noticia.png"
        )
        self.assertEquals(str(self.empresa), "Empresa")
