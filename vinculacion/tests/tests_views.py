from django.test import TestCase
from usuarios.models import User, TipoUsuario
from empresas.models import Empresa
from instituciones_educativas.models import InstitucionEducativa
from investigadores.models import (
    Investigador,
    NivelInvestigador,
    SolicitudTrabajo,
    Investigacion)
from django.urls import reverse
from helpers.usuarios_helpers import crear_usuario, crear_tipo_usuario
from helpers.vinculacion_helpers import (
    crear_noticia,
    crear_area_conocimiento,
    crear_categoria,
    crear_solicitud_trabajo)
from helpers.investigadores_helpers import (
    crear_nivel_investigador, crear_investigador)
from helpers.instituciones_educativas_helpers import (
    crear_institucion_educativa)
from helpers.empresas_helpers import crear_empresa


class TestCrearSolicitud(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCrearSolicitud, cls).setUpClass()
        cls.tipo_investigador = TipoUsuario.objects.create(
            tipo="Investigador")
        cls.usuario_investigador = User.objects.create(
            username="Prueba",
            email="asd@asd.com",
            is_active=True,
            tipo_usuario=cls.tipo_investigador,
            aprobado=True)
        cls.usuario_investigador.set_password("test")
        cls.usuario_investigador.save()
        cls.usuario_visitante = User.objects.create(
            username="Visitante",
            email="inv@inv.com",
            is_active=True,
            tipo_usuario=cls.tipo_investigador)
        cls.usuario_visitante.set_password("test")
        cls.usuario_visitante.save()
        cls.nivel_1 = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="lorem"
        )
        cls.investigador = Investigador.objects.create(
            nivel=cls.nivel_1,
            user=cls.usuario_investigador,
            curp="BEGE010204HZSLNLA5",
            latitud=0,
            longitud=0,
            codigo_postal="98613",
            municipio=0,
            colonia="Las joyas",
            calle="Esmeralda",
            numero_exterior=35,
            acerca_de="lorem"
        )

    def test_datos_completos(self):
        self.client.login(username="Visitante", password="test")
        self.client.post(
            reverse(
                "vinculacion:solicitud_trabajo_nueva",
                kwargs={
                    "investigador_id": self.investigador.pk
                }
            ),
            {
                "descripcion": "test",
                "titulo": "test"
            }
        )

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 1)

    def test_datos_titulo_vacio(self):
        self.client.login(username="Visitante", password="test")
        try:
            self.client.post(
                reverse(
                    "vinculacion:solicitud_trabajo_nueva",
                    kwargs={
                        "investigador_id": self.investigador.pk
                    }
                ),
                {
                    "descripcion": "test",
                    "titulo": ""
                }
            )
        except Exception:
            pass

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 0)

    def test_datos_titulo_largo(self):
        self.client.login(username="Visitante", password="test")
        try:
            self.client.post(
                reverse(
                    "vinculacion:solicitud_trabajo_nueva",
                    kwargs={
                        "investigador_id": self.investigador.pk
                    }
                ),
                {
                    "descripcion": "test",
                    "titulo": "a"*201
                }
            )
        except Exception:
            pass

        self.assertEquals(SolicitudTrabajo.objects.all().count(), 0)

    def test_datos_no_titulo(self):
        self.client.login(username="Visitante", password="test")
        try:
            self.client.post(
                reverse(
                    "vinculacion:solicitud_trabajo_nueva",
                    kwargs={
                        "investigador_id": self.investigador.pk
                    }
                ),
                {
                    "descripcion": "test",
                }
            )
        except Exception:
            pass

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 0)

    def test_datos_descripcion_vacio(self):
        self.client.login(username="Visitante", password="test")
        try:
            self.client.post(
                reverse(
                    "vinculacion:solicitud_trabajo_nueva",
                    kwargs={
                        "investigador_id": self.investigador.pk
                    }
                ),
                {
                    "descripcion": "",
                    "titulo": "prueba"
                }
            )
        except Exception:
            pass

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 0)

    def test_datos_descripcion_largo(self):
        self.client.login(username="Visitante", password="test")
        try:
            self.client.post(
                reverse(
                    "vinculacion:solicitud_trabajo_nueva",
                    kwargs={
                        "investigador_id": self.investigador.pk
                    }
                ),
                {
                    "descripcion": "a"*5001,
                    "titulo": "prueba"
                }
            )
        except Exception:
            pass

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 0)

    def test_datos_no_descripcion(self):
        self.client.login(username="Visitante", password="test")
        try:
            self.client.post(
                reverse(
                    "vinculacion:solicitud_trabajo_nueva",
                    kwargs={
                        "investigador_id": self.investigador.pk
                    }
                ),
                {
                    "titulo": "prueba"
                }
            )
        except Exception:
            pass

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 0)

    def test_datos_completos_mismo_investigador(self):
        self.client.login(username="Prueba", password="test")
        self.client.post(
            reverse(
                "vinculacion:solicitud_trabajo_nueva",
                kwargs={
                    "investigador_id": self.investigador.pk
                }
            ),
            {
                "descripcion": "test",
                "titulo": "test"
            }
        )

        self.assertEquals(len(SolicitudTrabajo.objects.all()), 0)


class TestResponderSolicitud(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestResponderSolicitud, cls).setUpClass()
        cls.tipo_investigador = TipoUsuario.objects.create(
            tipo="Investigador")
        cls.usuario_investigador = User.objects.create(
            username="Prueba",
            email="asd@asd.com",
            is_active=True,
            tipo_usuario=cls.tipo_investigador,
            aprobado=True)
        cls.usuario_investigador.set_password("test")
        cls.usuario_investigador.save()
        cls.usuario_visitante = User.objects.create(
            username="Visitante",
            email="inv@inv.com",
            is_active=True,
            tipo_usuario=cls.tipo_investigador)
        cls.usuario_visitante.set_password("test")
        cls.usuario_visitante.save()
        cls.nivel_1 = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="lorem"
        )
        cls.investigador = Investigador.objects.create(
            nivel=cls.nivel_1,
            user=cls.usuario_investigador,
            curp="BEGE010204HZSLNLA5",
            latitud=0,
            longitud=0,
            codigo_postal="98613",
            municipio=0,
            colonia="Las joyas",
            calle="Esmeralda",
            numero_exterior=35,
            acerca_de="lorem"
        )
        cls.solicitud = SolicitudTrabajo.objects.create(
            descripcion="Solicitud de ejemplo",
            titulo="Solicitud",
            usuario_a_vincular=cls.investigador,
            usuario_solicitante=cls.usuario_visitante,
            estado="E",
        )

    def test_aceptar_solicitud_id_valido_investigador(self):
        self.client.login(username="Prueba", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:aceptar_solicitud",
                kwargs={"pk": self.solicitud.pk},
            )
        )

        self.assertEquals(r.status_code, 302)

    def test_aceptar_solicitud_id_invalido_investigador(self):
        self.client.login(username="Prueba", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:aceptar_solicitud",
                kwargs={"pk": 5},
            )
        )

        self.assertEquals(r.status_code, 404)

    def test_rechazar_solicitud_id_valido_investigador(self):
        self.client.login(username="Prueba", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:rechazar_solicitud",
                kwargs={"pk": self.solicitud.pk},
            )
        )

        self.assertEquals(r.status_code, 302)

    def test_rechazar_solicitud_id_invalido_investigador(self):
        self.client.login(username="Prueba", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:rechazar_solicitud",
                kwargs={"pk": 5},
            )
        )

        self.assertEquals(r.status_code, 404)

    def test_aceptar_solicitud_id_valido_no_autorizado(self):
        self.client.login(username="Visitante", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:aceptar_solicitud",
                kwargs={"pk": self.solicitud.pk},
            )
        )

        self.assertEquals(r.status_code, 404)

    def test_aceptar_solicitud_id_invalido_no_autorizado(self):
        self.client.login(username="Visitante", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:aceptar_solicitud",
                kwargs={"pk": 5},
            )
        )

        self.assertEquals(r.status_code, 404)

    def test_rechazar_solicitud_id_valido_no_autorizado(self):
        self.client.login(username="Visitante", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:rechazar_solicitud",
                kwargs={"pk": self.solicitud.pk},
            )
        )

        self.assertEquals(r.status_code, 404)

    def test_rechazar_solicitud_id_invalido_no_autorizado(self):
        self.client.login(username="Visitante", password="test")
        r = self.client.get(
            reverse(
                "vinculacion:rechazar_solicitud",
                kwargs={"pk": 5},
            )
        )

        self.assertEquals(r.status_code, 404)


class TestSolicitarIngresoInvestigador(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='prueba-investigador', password='12345')
        self.usuario.save()
        self.client.login(
            username='prueba-investigador', password='12345')
        crear_nivel_investigador(1, "Nivel 1")

    def test_solicitar_ingreso(self):
        response = self.client.get('/perfil')
        self.assertEqual(response.status_code, 200)

    def test_solicitar_ingreso_investigador_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            datos = {'curp': 'AUCJ011020HZSGRVA1', 'codigo_postal': '99390',
                     'municipio': 19,
                     'colonia': 'Alamitos',
                     'calle': 'Mezquite', 'numero_exterior': '29',
                     'acerca_de': 'Info', 'imagen': imagen}
            self.client.post('/formularios/investigador', datos)
            self.assertEquals(
                Investigador.objects.count(), 1)

    def test_solicitar_ingreso_investigador_direccion_invalida(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            datos = {'curp': 'AUCJ011020HZSGRVA1', 'codigo_postal': '99393',
                     'municipio': 15,
                     'colonia': 'Durazno', 'calle': 'Frutas',
                     'numero_exterior': '229',
                     'acerca_de': 'Info', 'imagen': imagen}
            self.client.post('/formularios/investigador', datos)
            self.assertEquals(
                Investigador.objects.count(), 0)


class TestSolicitarIngresoEmpresa(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='prueba-empresa', password='12345')
        self.usuario.save()
        self.client.login(
            username='prueba-empresa', password='12345')
        area = crear_area_conocimiento("Ingeniería", "Las ingenierías")
        crear_categoria("Software", area, "El software")

    def test_solicitar_ingreso_empresa_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            datos = {'nombre_empresa': 'Empresa', 'codigo_postal': '99390',
                     'municipio': 19,
                     "especialidades": [1], 'colonia': 'Alamitos',
                     'calle': 'Mezquite',
                     'numero_exterior': '29', 'acerca_de': 'Info',
                     'imagen': imagen}
            self.client.post('/formularios/empresa', datos)
            self.assertEquals(
                Empresa.objects.count(), 1)

    def test_solicitar_ingreso_empresa_direccion_invalida(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            datos = {
                'nombre_empresa': 'Empresa',
                'codigo_postal': '99390',
                'municipio': 19,
                "especialidades": [1],
                'colonia': 'Durazno',
                'calle': 'Frutas',
                'numero_exterior': '229',
                'acerca_de': 'Info',
                'imagen': imagen
            }
            self.client.post(
                '/formularios/empresa',
                datos
            )
            self.assertEquals(
                Empresa.objects.count(), 0)


class TestSolicitarIngresoInstitucionEducativa(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='prueba-institucion', password='12345')
        self.usuario.save()
        self.client.login(
            username='prueba-institucion', password='12345')
        area = crear_area_conocimiento("Ingeniería", "Las ingenierías")
        crear_categoria("Software", area, "El software")
        nivel = crear_nivel_investigador(1, "Uno")
        tipo_investigador = crear_tipo_usuario("Investigador")
        usuario_investigador = crear_usuario(
            "usuario-investigador",
            "inv@inv.com",
            "12345678",
            tipo_investigador
        )
        crear_investigador(
            usuario=usuario_investigador,
            nivel=nivel,
            curp="AUCJ011020HZSGRVA1",
            latitud=0,
            longitud=0,
            codigo_postal=99390,
            municipio=20,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy un investigador"
        )

    def test_solicitar_ingreso_institucion_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            datos = {'nombre_institucion': 'Institucion',
                     'codigo_postal': '99390', 'municipio': 19,
                     "especialidades": [1],
                     'miembros': [2], 'colonia': 'Alamitos',
                     'calle': 'Mezquite',
                     'numero_exterior': '29',
                     'acerca_de': 'Info', 'imagen': imagen}
            self.client.post(
                '/formularios/institucion_educativa', datos)
            self.assertEquals(
                InstitucionEducativa.objects.count(), 1)

    def test_solicitar_ingreso_institucion_direccion_invalida(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            datos = {'nombre_institucion': 'Institucion',
                     'codigo_postal': '99350', 'municipio': 19,
                     "especialidades": [1], 'miembros': [2],
                     'colonia': 'Durazno', 'calle': 'Frutas',
                     'numero_exterior': '239', 'acerca_de': 'Info',
                     'imagen': imagen}
            self.client.post('/formularios/institucion_educativa', datos)
            self.assertEquals(
                InstitucionEducativa.objects.count(), 0)


class TestActualizarPerfilInvestigador(TestCase):
    def setUp(self):
        tipo_investigador = crear_tipo_usuario("Investigador")
        self.usuario_investigador = crear_usuario(
            usuario='prueba-investigador', correo="prueba@prueba.com",
            contra='12345', tipo=tipo_investigador, aprobado=True)
        self.usuario_investigador.save()
        self.client.login(
            username='prueba-investigador', password='12345')
        nivel_1 = crear_nivel_investigador(1, "Nivel 1")
        self.investigador = crear_investigador(
            usuario=self.usuario_investigador,
            nivel=nivel_1,
            curp="AUCJ011020HZSGRVA1",
            codigo_postal=99390,
            municipio=19,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy un investigador"
        )

    def test_actualizar_perfil_investigador_datos_correctos(self):
        datos = {
            'curp': "AUCJ011020HZSGRVA1",
            'codigo_postal': 99390,
            'municipio': 19,
            'colonia': "Alamitos",
            'calle': "Mezquite",
            'numero_exterior': 29,
            'acerca_de': "Hola"
        }
        respuesta = self.client.post(
            "/formularios/investigador/actualizar", datos)
        self.assertEqual(respuesta.status_code, 302)

    def test_actualizar_perfil_investigador_datos_incorrectos(self):
        datos = {
            'curp': "AUCJ011020HZSGRVA1",
            'codigo_postal': 99390,
            'municipio': 19,
            'colonia': "Alamitos",
            'calle': "Mezquite",
            'numero_exterior': 29,
            'acerca_de': " "
        }
        respuesta = self.client.post(
            "/formularios/investigador/actualizar", datos)
        self.assertEqual(respuesta.status_code, 200)

    def test_actualizar_perfil_investigador_localizacion_invalida(self):
        datos = {
            'curp': "AUCJ011020HZSGRVA1",
            'codigo_postal': 99390,
            'municipio': 2,
            'colonia': "Alamos",
            'calle': "Mezquites",
            'numero_exterior': 329,
            'acerca_de': "Hola"
        }
        respuesta = self.client.post(
            "/formularios/investigador/actualizar", datos)
        self.assertEqual(respuesta.status_code, 200)


class TestActualizarPerfilInstitucionEducativa(TestCase):
    def setUp(self):
        tipo_institucion = crear_tipo_usuario("Institucion Educativa")
        self.usuario_institucion = crear_usuario(
            usuario='prueba-institucion',
            correo="prueba@prueba.com",
            contra='12345', tipo=tipo_institucion, aprobado=True)
        self.usuario_institucion.save()
        self.client.login(
            username='prueba-institucion', password='12345')
        tipo_investigador = crear_tipo_usuario("Investigador")
        usuario_investigador = crear_usuario(
            "Investigador", "prueba-investigador@prueba.com",
            "prueba", tipo_investigador, aprobado=True)
        area_conocimiento = crear_area_conocimiento(
            "Ingeniería", "Sobre ingeniería")
        categoria = crear_categoria(
            "Software", area_conocimiento, "Sobre software")
        nivel_1 = crear_nivel_investigador(1, "Nivel 1")
        investigador = crear_investigador(
            usuario=usuario_investigador,
            nivel=nivel_1,
            curp="AUCJ011020HZSGRVA1",
            latitud=0,
            longitud=0,
            codigo_postal=99390,
            municipio=19,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy un investigador"
        )
        self.institucion_educativa = crear_institucion_educativa(
            encargado=self.usuario_institucion,
            nombre_institucion="Institución Prueba",
            especialidades=[categoria],
            miembros=[investigador],
            codigo_postal=99390,
            municipio=19,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy una institución"
        )

    def test_actualizar_perfil_institucion_datos_correctos(self):
        datos = {
            'nombre_institucion': "Institución Prueba",
            'especialidades': [1],
            'miembros': [2],
            'codigo_postal': 99390,
            'municipio': 19,
            'colonia': "Alamitos",
            'calle': "Mezquite",
            'numero_exterior': 29,
            'acerca_de': "Soy una institución loca"
        }
        respuesta = self.client.post(
            "/formularios/institucion_educativa/actualizar", datos)
        self.assertEqual(respuesta.status_code, 302)

    def test_actualizar_perfil_institucion_datos_incorrectos(self):
        datos = {
            'nombre_institucion': "Institución Prueba",
            'especialidades': [1],
            'miembros': [2],
            'codigo_postal': 99390,
            'municipio': 19,
            'colonia': "Alamitos",
            'calle': "Mezquite",
            'numero_exterior': 29,
            'acerca_de': " "
        }
        respuesta = self.client.post(
            "/formularios/institucion_educativa/actualizar", datos)
        self.assertEqual(respuesta.status_code, 200)

    def test_actualizar_perfil_institucion_localizacion_invalida(self):
        datos = {
            'nombre_institucion': "Institución Prueba",
            'especialidades': [1],
            'miembros': [2],
            'codigo_postal': 99393,
            'municipio': 13,
            'colonia': "Duro",
            'calle': "Mezquitestes",
            'numero_exterior': 298,
            'acerca_de': "Soy una institución loca"
        }
        respuesta = self.client.post(
            "/formularios/institucion_educativa/actualizar", datos)
        self.assertEqual(respuesta.status_code, 200)


class TestActualizarPerfilEmpresa(TestCase):
    def setUp(self):
        tipo_empresa = crear_tipo_usuario("Empresa")
        usuario_encargado = crear_usuario(
            usuario='prueba-empresa', correo="prueba@prueba.com",
            contra='12345', tipo=tipo_empresa, aprobado=True)
        usuario_encargado.save()
        self.client.login(
            username='prueba-empresa', password='12345')
        area_conocimiento = crear_area_conocimiento(
            "Ingeniería", "Sobre ingeniería")
        categoria = crear_categoria(
            "Software", area_conocimiento, "Sobre software")
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

    def test_actualizar_perfil_empresa_datos_correctos(self):
        datos = {
            'nombre_empresa': "Empresa Prueba",
            'especialidades': [1],
            'codigo_postal': 99390,
            'municipio': 19,
            'colonia': "Alamitos",
            'calle': "Mezquite",
            'numero_exterior': 29,
            'acerca_de': "Soy una empresa loca"
        }
        respuesta = self.client.post(
            "/formularios/empresa/actualizar", datos)
        self.assertEqual(respuesta.status_code, 302)

    def test_actualizar_perfil_empresa_datos_incorrectos(self):
        datos = {
            'nombre_empresa': "Empresa Prueba",
            'especialidades': [1],
            'codigo_postal': 99390,
            'municipio': 19,
            'colonia': "Alamitos",
            'calle': "Mezquite",
            'numero_exterior': 29,
            'acerca_de': " "
        }
        respuesta = self.client.post(
            "/formularios/empresa/actualizar",
            datos)
        self.assertEqual(respuesta.status_code, 200)

    def test_actualizar_perfil_empresa_localizacion_invalida(self):
        datos = {
            'nombre_empresa': "Empresa Prueba",
            'especialidades': [1],
            'codigo_postal': 99395,
            'municipio': 16,
            'colonia': "Alamenios",
            'calle': "Rock",
            'numero_exterior': 20,
            'acerca_de': "Soy una empresa loca"
        }
        respuesta = self.client.post(
            "/formularios/empresa/actualizar", datos)
        self.assertEqual(respuesta.status_code, 200)


class TestVistaHistorialTrabajos(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_vista_historial_trabajos(self):
        response = self.client.get('/perfil/trabajos/historial')
        self.assertEqual(response.status_code, 200)

    def test_vista_historial_trabajos_sin_login(self):
        self.client.logout()
        response = self.client.get('/perfil/trabajos/historial')
        self.assertEqual(response.status_code, 302)

    def test_vista_historial_trabajos_sin_investigador(self):
        usuario = User.objects.get(username='testuser')
        usuario.delete()
        response = self.client.get('/perfil/trabajos/historial')
        self.assertEqual(response.status_code, 302)


class TestVistaTrabajosEnCurso(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_vista_trabajos_en_curso(self):
        response = self.client.get('/perfil/trabajos')
        self.assertEqual(response.status_code, 200)

    def test_vista_trabajos_en_curso_sin_login(self):
        self.client.logout()
        response = self.client.get('/perfil/trabajos')
        self.assertEqual(response.status_code, 302)

    def test_vista_trabajos_en_curso_sin_investigador(self):
        usuario = User.objects.get(username='testuser')
        usuario.delete()
        response = self.client.get('/perfil/trabajos')
        self.assertEqual(response.status_code, 302)


class TestVistaRechazarSolicitud(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', passworaceptard='12345')

    def test_vista_rechazar_solicitud_sin_login(self):
        self.client.logout()
        response = self.client.get('/perfil/trabajos/rechazar/1')
        self.assertEqual(response.status_code, 404)

    def test_vista_rechazar_solicitud_sin_investigador(self):
        usuario = User.objects.get(username='testuser')
        usuario.delete()
        response = self.client.get('/perfil/trabajos/rechazar/1')
        self.assertEqual(response.status_code, 404)


class TestVistaAceptarSolicitud(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_vista_aceptar_solicitud_sin_login(self):
        self.client.logout()
        response = self.client.get('/perfil/trabajos/aprobar/1')
        self.assertEqual(response.status_code, 404)

    def test_vista_aceptar_solicitud_sin_investigador(self):
        usuario = User.objects.get(username='testuser')
        usuario.delete()
        response = self.client.get('/perfil/trabajos/aprobar/1')
        self.assertEqual(response.status_code, 404)


class TestSolicitarTrabajoNuevo(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_solicitar_trabajo_nuevo_sin_login(self):
        self.client.logout()
        response = self.client.get('/formularios/solicitudTrabajo/')
        self.assertEqual(response.status_code, 404)

    def test_solicitar_trabajo_nuevo_sin_investigador(self):
        usuario = User.objects.get(username='testuser')
        usuario.delete()
        response = self.client.get('/formularios/solicitudTrabajo/')
        self.assertEqual(response.status_code, 404)


class TestConsultaMapa(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_consultar_mapa_loggeado(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_consultar_mapa_no_loggeado(self):
        self.client.logout()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)


class TestEliminarUsuario(TestCase):
    def setUp(self):
        usuario = User.objects.create_user(
            username='testuser', password='12345')
        usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_eliminar_cuenta(self):
        self.client.post('/perfil/eliminar')
        self.assertEqual(User.objects.count(), 0)


class TestInstitucionEducativaMiembros(TestCase):
    def setUp(self):
        pass
        self.nivel = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="XD"
        )
        self.usuario_institucion = User.objects.create(
            username='testuser',
            aprobado=True,
            is_active=True,
            tipo_usuario=TipoUsuario.objects.get(tipo="Institucion Educativa"),
            email="test@test.com",
        )
        self.institucion = InstitucionEducativa.objects.create(
            encargado=self.usuario_institucion,
            acerca_de="a",
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las Joyas",
            latitud=0,
            longitud=0,
            municipio=16,
            nombre_institucion="Institucioncita",
            numero_exterior=35
        )
        self.usuario_investigador = User.objects.create(
            username='user_investigador',
            aprobado=True,
            is_active=True,
            email="test2@test.com",
            tipo_usuario=TipoUsuario.objects.get(tipo="Investigador")
        )
        self.investigador = Investigador.objects.create(
            acerca_de="a",
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las Joyas",
            curp="BEGE010204HZSLNLA5",
            municipio=16,
            numero_exterior=35,
            latitud=0,
            longitud=0,
            user=self.usuario_investigador,
            nivel=self.nivel,
        )
        self.usuario_institucion.set_password("12345")
        self.usuario_institucion.save()
        self.usuario_investigador.set_password("12345")
        self.usuario_investigador.save()
        self.client.login(username='user_investigador', password='12345')
        self.client.get(
            f"/investigador/solicitud_ingreso/{self.institucion.pk}")
        self.client.login(username='testuser', password='12345')

    def test_listar_solicitud_miembros(self):
        r = self.client.get("/institucion_educativa/solicitud_ingreso")
        self.assertEquals(r.status_code, 200)

    def test_listar_miembros(self):
        r = self.client.get("/institucion_educativa/miembros")
        self.assertEquals(r.status_code, 200)

    def test_aceptar_solicitud_miembro(self):
        self.client.get(
            "/institucion_educativa/solicitud_ingreso/" +
            f"{self.investigador.pk}/1")
        self.assertEquals(
            len(
                InstitucionEducativa.objects.get(
                    pk=self.institucion.pk).miembros.all()),
            1)

    def test_rechazar_solicitud_miembro(self):
        self.client.get(
            "/institucion_educativa/solicitud_ingreso/" +
            f"{self.investigador.pk}/0")
        self.assertEquals(
            len(
                InstitucionEducativa.objects.get(
                    pk=self.institucion.pk).miembros.all()),
            0)

    def test_eliminar_miembro(self):
        self.client.get(
            "/institucion_educativa/solicitud_ingreso/" +
            f"{self.investigador.pk}/1")
        self.client.get(
            "/institucion_educativa/miembros/eliminar/" +
            f"{self.investigador.pk}")
        self.assertEquals(
            len(
                InstitucionEducativa.objects.get(
                    pk=self.institucion.pk).miembros.all()),
            0)


class TestConsultarNoticias (TestCase):
    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        self.escritor = crear_usuario(
            "escritor", "escritor@escritor.com", "12345678")
        self.noticia = crear_noticia(
            "Noticia", "Contenido", self.escritor, "/noticias/noticia.png")

    def test_consultar_listado_noticias(self):
        respuesta = self.client.get("/noticias")
        self.assertEquals(respuesta.status_code, 200)

    def test_consultar_detalle_noticia(self):
        respuesta = self.client.get(f"/noticias/{self.noticia.pk}")
        self.assertEquals(respuesta.status_code, 200)


class TestConsultarUsuarios(TestCase):
    def setUp(self):
        nivel = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="XD"
        )
        usuario = User.objects.create(
            username="rootardo",
            aprobado=True,
            email="root@tardo.com",
            is_active=True,
            tipo_usuario=TipoUsuario.objects.get(tipo="Investigador")
        )
        usuario_inst = User.objects.create(
            username="wow",
            aprobado=True,
            email="wow@tardo.com",
            is_active=True,
            tipo_usuario=TipoUsuario.objects.get(tipo="Institucion Educativa")
        )
        usuario.set_password("12345678")
        usuario.save()
        Investigador.objects.create(
            nivel=nivel,
            acerca_de="a",
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las joyas",
            curp="BEGE010204HZSLNLA5",
            latitud=0,
            longitud=0,
            municipio=16,
            numero_exterior=35,
            user=usuario
        )
        InstitucionEducativa.objects.create(
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las joyas",
            latitud=0,
            longitud=0,
            municipio=16,
            numero_exterior=35,
            acerca_de="asd",
            encargado=usuario_inst,
            nombre_institucion="Gokuuu"
        )
        self.client.login(username='rootardo', password='12345678')

    def test_consultar_investigadores(self):
        r = self.client.get("/investigadores")
        self.assertEquals(r.status_code, 200)

    def test_consultar_empresas(self):
        r = self.client.get("/empresas")
        self.assertEquals(r.status_code, 200)

    def test_consultar_instituciones_educativas(self):
        r = self.client.get("/instituciones_educativas/")
        self.assertEquals(r.status_code, 200)


class TestConsultaPerfilPublico(TestCase):
    def setUp(self):
        self.usuario_investigador = User.objects.create(
            username='user_investigador',
            aprobado=True,
            is_active=True,
            email="test2@test.com",
            tipo_usuario=TipoUsuario.objects.get(
                tipo="Investigador")
        )
        self.nivel = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="XD"
        )
        self.investigador = Investigador.objects.create(
            acerca_de="a",
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las Joyas",
            curp="BEGE010204HZSLNLA5",
            municipio=16,
            numero_exterior=35,
            latitud=0,
            longitud=0,
            user=self.usuario_investigador,
            nivel=self.nivel,
        )
        self.investigador.save()
        self.usuario_investigador.set_password("12345678")
        self.usuario_investigador.save()

    def test_consultar_perfil_investigador(self):
        self.client.login(
            username=self.usuario_investigador.username,
            password='12345678'
                    )
        r = self.client.get(
            f"/investigadores/{self.usuario_investigador.pk}")
        self.assertEquals(r.status_code, 200)


class TestConsultaInvestigacionNueva(TestCase):
    def setUp(self):
        self.usuario_investigador = User.objects.create(
            username='user_investigador',
            aprobado=True,
            is_active=True,
            email="test2@test.com",
            tipo_usuario=TipoUsuario.objects.get(
                tipo="Investigador")
        )
        self.nivel = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="XD"
        )
        self.investigador = Investigador.objects.create(
            acerca_de="a",
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las Joyas",
            curp="BEGE010204HZSLNLA5",
            municipio=16,
            numero_exterior=35,
            latitud=0,
            longitud=0,
            user=self.usuario_investigador,
            nivel=self.nivel,
        )

        self.investigador.save()
        self.usuario_investigador.set_password("12345678")
        self.usuario_investigador.save()
        self.area = crear_area_conocimiento("Ingeniería", "Las ingenierías")
        self.categoria = crear_categoria("Software", self.area, "El software")

    def test_crear_investigacion_status_code(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.get("/formularios/investigacion")
        self.assertEquals(r.status_code, 200)

    def test_crear_investigacion(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.post("/formularios/investigacion", {
            "titulo": "Investigacion de prueba",
            "categoria": [7],
            "autores": [self.investigador.pk],
            "contenido": "Contenido de prueba",
        })
        self.assertEquals(r.status_code, 200)

    def test_crea_investigacion_autor_no_existe(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.post("/formularios/investigacion", {
            "titulo": "Investigacion de prueba",
            "categoria": self.categoria.pk,
            "autores": -11,
            "contenido": "Contenido de prueba"
        })
        self.assertEquals(r.status_code, 200)


class cambioEstadoTest(TestCase):
    def setUp(self):
        self.nivel = crear_nivel_investigador(1, "Uno")
        self.tipo_investigador = crear_tipo_usuario("Investigador")
        self.usuario_investigador = crear_usuario(
            "usuario-investigador",
            "inv@inv.com",
            "12345678",
            self.tipo_investigador
        )
        self.usuario_contratador = crear_usuario(
            "usuario-contratador",
            "mailC@mail.com",
            "12345678",
            self.tipo_investigador
        )
        self.investigador = crear_investigador(
            usuario=self.usuario_investigador,
            nivel=self.nivel,
            curp="AUCJ011020HZSGRVA1",
            latitud=0,
            longitud=0,
            codigo_postal=99390,
            municipio=20,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy un investigador"
        )
        self.investigador2 = crear_investigador(
            usuario=self.usuario_contratador,
            nivel=self.nivel,
            curp="AUCJ011020HZSGRVA1",
            latitud=0,
            longitud=0,
            codigo_postal=99390,
            municipio=20,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy un investigador"
        )
        self.investigador.save()
        self.investigador2.save()
        self.solicitud_trabajo = crear_solicitud_trabajo(
            titulo="Solicitud de trabajo",
            descripcion="Solicitud de trabajo",
            usuario_a_vincular=self.investigador,
            usuario_solicitante=self.usuario_contratador
        )
        self.solicitud_trabajo.save()

    def test_cambio_estado_p(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.post(
            f"/perfil/trabajos/cambiar_estado/{self.solicitud_trabajo.pk}/P")
        self.assertEquals(r.status_code, 302)

    def test_cambio_estado_c(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.post(
            f"/perfil/trabajos/cambiar_estado/{self.solicitud_trabajo.pk}/C")
        self.assertEquals(r.status_code, 302)

    def test_cambio_estado_f(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.post(
            f"/perfil/trabajos/cambiar_estado/{self.solicitud_trabajo.pk}/F")
        self.assertEquals(r.status_code, 302)

    def test_cambio_estado_r(self):
        self.client.login(
            username=self.usuario_investigador.username, password='12345678')
        r = self.client.post(
            f"/perfil/trabajos/cambiar_estado/{self.solicitud_trabajo.pk}/R")
        self.assertEquals(r.status_code, 302)

    def test_cambio_estado_e(self):
        self.client.login(
            username=self.usuario_contratador.username, password='12345678')
        r = self.client.post(
            f"/perfil/trabajos/cambiar_estado/{self.solicitud_trabajo.pk}/E")
        self.assertEquals(r.status_code, 302)

    def test_cambio_estado_no_valido(self):
        self.client.login(
            username=self.usuario_contratador.username, password='12345678')
        r = self.client.post(
            f"/perfil/trabajos/cambiar_estado/{self.solicitud_trabajo.pk}/Z")
        self.assertEquals(r.status_code, 302)


class TestImportarInvestigacionesGoogleScholar(TestCase):
    def setUp(self):
        tipo_investigador = crear_tipo_usuario("Investigador")
        usuario_investigador = crear_usuario(
            usuario="prueba-investigador", correo="prueba@prueba.com",
            contra="12345678", tipo=tipo_investigador, aprobado=True)
        self.client.login(username="prueba-investigador", password="12345678")
        nivel_1 = crear_nivel_investigador(1, "Nivel 1")
        self.investigador = crear_investigador(
            usuario=usuario_investigador,
            nivel=nivel_1,
            curp="AUCJ011020HZSGRVA1",
            codigo_postal=99390,
            municipio=19,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy un investigador"
        )

    def test_perfil_investigaciones(self):
        self.client.get("/perfil/investigaciones")

    def test_importar_investigaciones_google_scholar(self):
        datos = {
            "profile-url":
                "https://scholar.google.com/citations?hl=en&user=YGnk7uoAAAAJ"
        }
        self.client.post("/perfil/investigaciones/fetch", datos)
        self.assertEqual(Investigacion.objects.count(), 1)

    def test_importar_investigaciones_google_scholar_perfil_inexistente(self):
        datos = {
            "profile-url": "link_perfil"
        }
        self.client.post("/perfil/investigaciones/fetch", datos)
        self.assertEqual(Investigacion.objects.count(), 0)
