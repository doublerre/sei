from django.test import TestCase
from usuarios.models import User, TipoUsuario
from investigadores.models import Investigador, NivelInvestigador
from empresas.models import Empresa
from vinculacion.models import Noticia
from instituciones_educativas.models import InstitucionEducativa
from helpers.instituciones_educativas_helpers import (
    crear_institucion_educativa)
from helpers.usuarios_helpers import crear_usuario, crear_tipo_usuario
from helpers.vinculacion_helpers import (
    crear_area_conocimiento, crear_categoria, crear_noticia)
from helpers.investigadores_helpers import (
    crear_investigador, crear_nivel_investigador)
from helpers.empresas_helpers import crear_empresa


class TestCrudUsuario(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(
            username='testuser',
            aprobado=True,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email="test@test.com",
        )
        self.usuario.set_password("12345")
        self.usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_crear_usuario(self):
        usuario = {
            "username": "Elias",
            "password": "testiando",
            "email": "elias@redacted.com",
        }
        self.client.post("/administracion/usuarios/nuevo", usuario)
        self.assertEquals(User.objects.count(), 2)

    def test_editar_usuario(self):
        usuario = {
            "username": "Elias",
            "password": "testiando",
            "email": "elias@redacted.com",
        }
        self.client.post(
            f"/administracion/usuarios/editar/{self.usuario.pk}", usuario)
        self.assertEquals(
            User.objects.get(pk=self.usuario.pk).username, "Elias")

    def test_eliminar_usuario(self):
        self.client.post(
            f"/administracion/usuarios/eliminar/{self.usuario.pk}")
        self.assertEquals(User.objects.count(), 0)


class TestCRUDInvestigador(TestCase):
    def setUp(self):
        self.nivel = NivelInvestigador.objects.create(
            nivel=1,
            descripcion="XD"
        )
        self.usuario = User.objects.create(
            username='testuser',
            aprobado=True,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email="test@test.com",
        )
        self.usuario2 = User.objects.create(
            username='user_investigador',
            aprobado=True,
            is_staff=True,
            is_superuser=True,
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
            user=self.usuario2,
            nivel=self.nivel,
        )
        self.usuario.set_password("12345")
        self.usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_crear_investigador_direccion_valida(self):
        investigador = {
            "acerca_de": "a",
            "calle": "Esmeralda",
            "codigo_postal": 98613,
            "colonia": "Las Joyas",
            "curp": "BEGE010204HZSLNLA5",
            "municipio": 16,
            "numero_exterior": 35,
            "user": self.usuario.pk,
            "nivel": self.nivel.pk,
        }
        self.client.post(
            "/administracion/investigadores/nuevo", investigador)
        self.assertEquals(Investigador.objects.count(), 2)

    def test_crear_investigador_direccion_invalida(self):
        investigador = {
            "acerca_de": "a",
            "calle": "Esmeralda",
            "codigo_postal": 98613,
            "colonia": "Las Joyas",
            "curp": "BEGE010204HZSLNLA5",
            "municipio": 15,
            "numero_exterior": 35,
            "user": self.usuario.pk,
            "nivel": self.nivel.pk,
        }
        self.client.post(
            "/administracion/investigadores/nuevo", investigador)
        self.assertEquals(Investigador.objects.count(), 1)

    def test_editar_investigador_direccion_valida(self):
        investigador = {
            "acerca_de": "actualizado",
            "calle": "Esmeralda",
            "codigo_postal": 98613,
            "colonia": "Las Joyas",
            "curp": "BEGE010204HZSLNLA5",
            "municipio": 16,
            "numero_exterior": 35,
            "nivel": self.nivel.pk,
        }
        self.client.post(
            f"/administracion/investigadores/editar/{self.investigador.pk}",
            investigador)
        self.assertEquals(
            Investigador.objects.get(pk=self.investigador.pk).acerca_de,
            "actualizado")

    def test_editar_investigador_direccion_invalida(self):
        investigador = {
            "acerca_de": "actualizado",
            "calle": "Esmeralda",
            "codigo_postal": 98613,
            "colonia": "Las Joyas",
            "curp": "BEGE010204HZSLNLA5",
            "municipio": 15,
            "numero_exterior": 35,
            "nivel": self.nivel.pk,
        }
        self.client.post(
            f"/administracion/investigadores/editar/{self.investigador.pk}",
            investigador)
        self.assertEquals(
            Investigador.objects.get(pk=self.investigador.pk).acerca_de,
            "a")

    def test_eliminar_investigador(self):
        self.client.post(
            f"/administracion/investigadores/eliminar/{self.investigador.pk}")
        self.assertEquals(Investigador.objects.count(), 0)


class TestSolicitudEmpresa(TestCase):

    def setUp(self):
        self.usuario = User.objects.create(
            username='testuser',
            aprobado=True,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email="test@test.com",
        )
        self.usuario_empresa = User.objects.create(
            username='user_empresa',
            aprobado=False,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email="test2@test.com",
            tipo_usuario=TipoUsuario.objects.get(tipo="Empresa")
        )
        self.empresa = Empresa.objects.create(
            acerca_de="a",
            calle="Esmeralda",
            codigo_postal=98613,
            colonia="Las Joyas",
            municipio=16,
            numero_exterior=35,
            latitud=0,
            longitud=0,
            encargado=self.usuario_empresa,
            nombre_empresa="EmpresaPrueba"
        )
        self.usuario.set_password("12345")
        self.usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_aceptar_solicitud_empresa(self):
        self.client.get(
            f"/administracion/aprobar_perfil/{self.usuario_empresa.pk}")

        self.assertTrue(
            User.objects.get(pk=self.usuario_empresa.pk).aprobado)

    def test_rechazar_solicitud_empresa(self):
        self.client.post(
            f"/administracion/empresas/eliminar/{self.empresa.pk}")

        self.assertEquals(
            Empresa.objects.count(), 0)


class TestSolicitudInstitucionEducativa (TestCase):
    def setUp(self):
        self.admin = crear_usuario(
            "root",
            "root@root.com",
            "12345",
            superusuario=True,
            staff=True
        )
        self.tipo_institucion = crear_tipo_usuario("Institucion")
        self.tipo_investigador = crear_tipo_usuario("Investigador")
        self.usuario_institucion = crear_usuario(
            "prueba-institucion",
            "prueba-institucion@prueba.com", "prueba", self.tipo_institucion)
        self.usuario_investigador = crear_usuario(
            "Investigador", "prueba-investigador@prueba.com",
            "prueba", self.tipo_investigador)
        self.area_conocimiento = crear_area_conocimiento(
            "Ingeniería", "Sobre ingeniería")
        self.categoria = crear_categoria(
            "Software", self.area_conocimiento, "Sobre software")
        self.nivel_1 = crear_nivel_investigador(1, "Nivel 1")
        self.investigador = crear_investigador(
            usuario=self.usuario_investigador,
            nivel=self.nivel_1,
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
        self.institucion_educativa = crear_institucion_educativa(
            encargado=self.usuario_institucion,
            nombre_institucion="Institución Prueba",
            especialidades=[self.categoria],
            latitud=0,
            longitud=0,
            miembros=[self.investigador],
            codigo_postal=99390,
            municipio=20,
            colonia="Alamitos",
            calle="Mezquite",
            numero_exterior=29,
            acerca_de="Soy una institución"
        )
        self.client.login(username='root', password='12345')

    def test_aprobar_solicitud_institucion_educativa(self):
        self.client.get(
            f"/administracion/aprobar_perfil/{self.usuario_institucion.pk}")

        self.assertTrue(
            User.objects.get(pk=self.usuario_institucion.pk).aprobado)

    def test_rechazar_solicitud_institucion_educativa(self):
        self.client.post(
            "/administracion/instituciones_educativas/eliminar/" +
            f"{self.institucion_educativa.pk}")

        self.assertEquals(
            InstitucionEducativa.objects.count(), 0)


class TestCrearNoticia(TestCase):
    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        self.escritor = crear_usuario(
            "escritor", "escritor@escritor.com", "12345678")

    def test_crear_noticia_datos_incorrectos(self):
        noticia = {
            "titulo": "",
            "contenido": "",
            "escritor": "",
            "imagen": ""
        }
        self.client.post("/administracion/noticias/nuevo", noticia)
        self.assertEquals(Noticia.objects.count(), 0)

    def test_crear_noticia_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            noticia = {
                "titulo": "Noticia",
                "contenido": "Contenido",
                "escritor": 2,
                "imagen": imagen
            }
            self.client.post("/administracion/noticias/nuevo", noticia)

            self.assertEquals(Noticia.objects.count(), 1)


class TestEditarNoticia(TestCase):
    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        self.escritor = crear_usuario(
            "escritor", "escritor@escritor.com",
            "12345678", aprobado=True, superusuario=True, staff=True)
        self.noticia = crear_noticia(
            "Noticia", "Contenido", self.escritor, "/noticias/noticia.png")

    def test_editar_noticia_datos_incorrectos(self):
        noticiaEditada = {
            "titulo": "",
            "contenido": "",
            "escritor": "",
            "imagen": ""
        }
        self.client.post(
            f"/administracion/noticias/editar/{self.noticia.pk}",
            noticiaEditada)
        self.assertEquals(
            Noticia.objects.get(pk=self.noticia.pk).titulo, "Noticia")

    def test_editar_noticia_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            noticia = {
                "titulo": "Noticia modificada",
                "contenido": "Contenido",
                "escritor": 2,
                "imagen": imagen
            }
            self.client.post(
                f"/administracion/noticias/editar/{self.noticia.pk}", noticia)

            self.assertEquals(
                Noticia.objects.get(
                    pk=self.noticia.pk).titulo, "Noticia modificada")


class TestEliminarNoticia(TestCase):

    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        self.escritor = crear_usuario(
            "escritor", "escritor@escritor.com", "12345678")
        self.noticia = crear_noticia(
            "Noticia", "Contenido", self.escritor, "/noticias/noticia.png")

    def test_eliminar_noticia(self):
        self.client.post(
            f"/administracion/noticias/eliminar/{self.noticia.pk}")
        self.assertEquals(Noticia.objects.count(), 0)


class TestCrearEmpresa(TestCase):
    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        area_conocimiento = crear_area_conocimiento(
            "Ingeniería", "Sobre ingeniería")
        crear_categoria("Software", area_conocimiento, "Sobre software")
        self.tipo_empresa = TipoUsuario.objects.get(tipo="Empresa")
        self.usuario_encargado = crear_usuario(
            usuario="encargado",
            correo="encargado@encargado.com",
            contra="12345678",
            tipo=self.tipo_empresa,
            aprobado=True
        )

    def test_crear_empresa_datos_incorrectos(self):
        empresa = {
            "encargado": ""
        }
        self.client.post("/administracion/empresas/nuevo", empresa)
        self.assertEquals(Empresa.objects.count(), 0)

    def test_crear_empresa_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            empresa = {
                'encargado': [1],
                'nombre_empresa': "Empresa",
                'codigo_postal': '99390',
                'municipio': 19,
                'especialidades': [1],
                'colonia': 'Alamitos',
                'calle': 'Mezquite',
                'numero_exterior': '29',
                'acerca_de': 'Info',
                'imagen': imagen
            }
            self.client.post("/administracion/empresas/nuevo", empresa)

            self.assertEquals(Empresa.objects.count(), 1)

    def test_crear_empresa_localizacion_invalida(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            empresa = {
                'encargado': [1],
                'nombre_empresa': "Empresa",
                'codigo_postal': '99390',
                'municipio': 15,
                'especialidades': [1],
                'colonia': 'Alamos',
                'calle': 'Mezquites',
                'numero_exterior': '229',
                'acerca_de': 'Info',
                'imagen': imagen
            }
            self.client.post("/administracion/empresas/nuevo", empresa)

            self.assertEquals(Empresa.objects.count(), 0)


class TestEditarEmpresa(TestCase):
    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        area_conocimiento = crear_area_conocimiento(
            "Ingeniería", "Sobre ingeniería")
        self.categoria = crear_categoria(
            "Software", area_conocimiento, "Sobre software")
        tipo_empresa = crear_tipo_usuario("Empresa")
        self.usuario_encargado = crear_usuario(
            usuario="encargado",
            correo="encargado@encargado.com",
            contra="12345678",
            tipo=tipo_empresa,
            aprobado=True
        )
        self.empresa = crear_empresa(
            encargado=self.usuario_encargado,
            nombre_empresa="Empresa",
            codigo_postal='99390',
            municipio=19,
            especialidades=[self.categoria],
            colonia='Alamitos',
            calle='Mezquite',
            numero_exterior='29',
            acerca_de='Info',
            imagen="/tmp/noticia.png"
        )

    def test_editar_empresa_datos_incorrectos(self):
        empresaEditada = {
            "encargado": " "
        }
        self.client.post(
            f"/administracion/empresas/editar/{self.empresa.pk}",
            empresaEditada)
        self.assertEquals(
            Empresa.objects.get(pk=self.empresa.pk).nombre_empresa, "Empresa")

    def test_editar_empresa_datos_correctos(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            empresa = {
                'encargado': [1],
                'nombre_empresa': "Empresa modificada",
                'codigo_postal': '99390',
                'municipio': 19,
                'especialidades': [1],
                'colonia': 'Alamitos',
                'calle': 'Mezquite',
                'numero_exterior': '29',
                'acerca_de': 'Info',
                'imagen': imagen
            }
            self.client.post(
                f"/administracion/empresas/editar/{self.empresa.pk}", empresa)
            self.assertEquals(
                Empresa.objects.get(
                    pk=self.empresa.pk).nombre_empresa, "Empresa modificada")

    def test_editar_empresa_localizacon_incorrecta(self):
        ruta_imagen = '/tmp/noticia.png'
        with open(ruta_imagen, 'rb') as imagen:
            empresa = {
                'encargado': [1],
                'nombre_empresa': "Empresa modificada",
                'codigo_postal': '99393',
                'municipio': 19,
                'especialidades': [1],
                'colonia': 'Durazno',
                'calle': 'Frutas',
                'numero_exterior': '295',
                'acerca_de': 'Info',
                'imagen': imagen
            }
            self.client.post(
                f"/administracion/empresas/editar/{self.empresa.pk}", empresa)
            self.assertEquals(
                Empresa.objects.get(
                    pk=self.empresa.pk).nombre_empresa, "Empresa")


class TestEliminarEmpresa(TestCase):

    def setUp(self):
        crear_usuario(usuario="root", correo="root@root.com",
                      contra="12345678", superusuario=True, staff=True)
        self.client.login(username='root', password='12345678')
        area_conocimiento = crear_area_conocimiento(
            "Ingeniería", "Sobre ingeniería")
        self.categoria = crear_categoria(
            "Software", area_conocimiento, "Sobre software")
        tipo_empresa = crear_tipo_usuario("Empresa")
        self.usuario_encargado = crear_usuario(
            usuario="encargado",
            correo="encargado@encargado.com",
            contra="12345678",
            tipo=tipo_empresa,
            aprobado=True
        )
        self.empresa = crear_empresa(
            encargado=self.usuario_encargado,
            nombre_empresa="Empresa",
            codigo_postal='99390',
            municipio=19,
            especialidades=[self.categoria],
            colonia='Alamitos',
            calle='Mezquite',
            numero_exterior='29',
            acerca_de='Info',
            imagen="/tmp/noticia.png"
        )

    def test_eliminar_empresa(self):
        self.client.post(
            f"/administracion/empresas/eliminar/{self.empresa.pk}")
        self.assertEquals(Empresa.objects.count(), 0)


class TestDashboard(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(
            username='testuser',
            aprobado=True,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            email="test@test.com",
        )
        self.usuario.set_password("12345")
        self.usuario.save()
        self.client.login(username='testuser', password='12345')

    def test_dashboard(self):
        r = self.client.get("/administracion/")
        self.assertEquals(r.status_code, 200)
