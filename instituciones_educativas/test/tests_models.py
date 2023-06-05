from django.test import TestCase
from instituciones_educativas.models import InstitucionEducativa
from usuarios.models import User


class InstitucionEducativaTestCase(TestCase):
    def setUp(self):
        self.encargado = User.objects.create(
            username="encargado",
            email="encargado@mail.com",
            password="admin",
            aprobado=True,)
        self.encargado.save()

        self.institucion = InstitucionEducativa.objects.create(
            encargado_id=self.encargado.pk,
            nombre_institucion="Instituto Tecnológico de Tijuana",
            latitud=32.500000,
            longitud=-117.080000,
            codigo_postal="22000",
            municipio=1,
            colonia="Colonia Centro",
            calle="Calle 5",
            numero_exterior=123,
            acerca_de="Acerca de",
        )

    def test_smoke(self):
        self.assertTrue(1+1, 2)

    def test_institucion_educativa(self):
        self.assertEqual(self.institucion.nombre_institucion, "Instituto " +
                         "Tecnológico de Tijuana")

    def test_institucion_educativa_str(self):
        self.assertEqual(str(self.institucion), "Instituto " +
                         "Tecnológico de Tijuana")

    def test_institucion_educativa_get_longitud(self):
        self.assertEqual(self.institucion.longitud, -117.080000)

    def test_institucion_educativa_get_latitud(self):
        self.assertEqual(self.institucion.latitud, 32.500000)

    def test_institucion_educativa_get_municipio(self):
        self.assertEqual(self.institucion.municipio, 1)
