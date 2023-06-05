from django.test import TestCase
from usuarios.models import User
from investigadores.models import (
    SolicitudTrabajo,
    NivelInvestigador,
    Investigador)
from django.utils import timezone
from vinculacion.helpers import (
    cancelar_trabajo,
    finalizar_trabajo,
    rechazar_trabajo,
    trabajo_en_proceso,
    trabajo_en_revision,
    enviar_correo_estado
    )


class TestSmoke(TestCase):
    def test_smoke(self):
        self.assertTrue(True)


class TestCambioEstados(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser', password='12345', email="test@mail.com")
        self.usuario.save()
        self.usuario2 = User.objects.create_user(
            username='testuser2', password='12345', email="test2@mail.com")
        self.usuario2.save()

        nivelinvestigadores = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="Descripcion",
        )
        nivelinvestigadores.save()

        self.investigador = Investigador.objects.create(
            user=self.usuario,
            nivel=nivelinvestigadores,
            curp='JISD770826MSPMTV51',
            latitud=0.0,
            longitud=0.0,
            codigo_postal=99360,
            municipio=1,
            colonia='Alamedas',
            calle='Jomulquillo',
            numero_exterior=22,
            acerca_de='Robamos tesis a domicilio'
        )
        self.investigador.save()

        self.solicitud = SolicitudTrabajo.objects.create(
            titulo="Titulo",
            usuario_a_vincular=self.investigador,
            usuario_solicitante=self.usuario2,
            estado='P',
            estado_investigador='P',
            estado_empleador='P',
            descripcion='test',
            fecha=timezone.now(),
            fecha_finalizado=timezone.now(),
        )
        self.solicitud.save()

    # Cancelar trabajo
    def test_cancelar_estado_empleado(self):
        cancelar_trabajo(self.solicitud.usuario_a_vincular.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado, 'C')

    def test_cancelar_estado_empleador(self):
        cancelar_trabajo(self.solicitud.usuario_solicitante.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado, 'C')

    # Finalizar trabajo
    def test_finalizar_estado_empleado(self):
        self.solicitud.estado = 'P'
        finalizar_trabajo(self.solicitud.usuario_a_vincular.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado, 'P')
        self.assertEqual(self.solicitud.estado_investigador, 'F')

    def test_finalizar_estado_empleador(self):
        self.solicitud.estado = 'P'
        finalizar_trabajo(
            self.solicitud.usuario_solicitante.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado, 'F')

    # Rechazar trabajo
    def test_rechazar_estado_empleador(self):
        rechazar_trabajo(self.solicitud.usuario_solicitante.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado_empleador, 'R')

    # Trabajo en proceso
    def test_trabajo_en_proceso(self):
        trabajo_en_proceso(
            self.solicitud.usuario_a_vincular.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado, 'P')

    # Trabajo en revision
    def test_trabajo_en_revision_empleado(self):
        trabajo_en_revision(
            self.solicitud.usuario_a_vincular.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado_investigador, 'E')

    def test_trabajo_en_revision_empleador(self):
        trabajo_en_revision(
            self.solicitud.usuario_solicitante.pk, self.solicitud)
        self.assertEqual(self.solicitud.estado_empleador, 'E')

    # Envio de correo
    def test_envio_correo(self):
        resultado = enviar_correo_estado(
            self.solicitud.pk, "Test",
            "Este es un mensaje de prueba",
            ["mail@mail.com"])
        self.assertTrue(resultado, True)
