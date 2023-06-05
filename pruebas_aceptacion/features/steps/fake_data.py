from behave import given
from investigadores.models import (
    NivelInvestigador,
    Investigador,
    Investigacion)
from vinculacion.models import Categoria, AreaConocimiento
from usuarios.models import User, TipoUsuario
from instituciones_educativas.models import (
    SolicitudIngreso,
    InstitucionEducativa)
from empresas.models import Empresa


def poblar_base_de_datos():
    if TipoUsuario.objects.count() != 3:
        TipoUsuario.objects.create(tipo="Investigador")
        TipoUsuario.objects.create(tipo="Empresa")
        TipoUsuario.objects.create(tipo="Institucion Educativa")
    NivelInvestigador.objects.create(
        nivel=1,
        descripcion="lorem"
    )
    User.objects.create(
        username="usuario_visitante",
        email="usuario@visitante.com",
        aprobado=False,
        is_active=True,
    )
    usuario_investigador = User.objects.create(
        username="usuario_investigador",
        email="usuario@investigador.com",
        aprobado=True,
        tipo_usuario=TipoUsuario.objects.get(tipo="Investigador"),
        is_active=True,
    )
    usuario_investigador.set_password("password1234")
    usuario_investigador.save()
    usuario_institucion = User.objects.create(
        username="usuario_institucion",
        email="usuario@institucion.com",
        aprobado=True,
        tipo_usuario=TipoUsuario.objects.get(tipo="Institucion Educativa"),
        is_active=True,
    )
    usuario_institucion.set_password("password1234")
    usuario_institucion.save()
    usuario_empresa = User.objects.create(
        username="usuario_empresa",
        email="usuario@empresa.com",
        aprobado=False,
        tipo_usuario=TipoUsuario.objects.get(tipo="Empresa"),
        is_active=True,
    )
    usuario_empresa.set_password("password1234")
    usuario_empresa.save()
    Investigador.objects.create(
        nivel=NivelInvestigador.objects.get(nivel=1),
        acerca_de="a",
        calle="Esmeralda",
        codigo_postal=98613,
        colonia="Las joyas",
        curp="BEGE010204HZSLNLA5",
        latitud=22.7546535,
        longitud=-102.4893209,
        municipio=16,
        numero_exterior=35,
        user=User.objects.get(username="usuario_investigador")
    )
    InstitucionEducativa.objects.create(
        acerca_de="a",
        calle="Esmeralda",
        codigo_postal=98613,
        colonia="Las joyas",
        encargado=usuario_institucion,
        latitud=0,
        longitud=0,
        municipio=16,
        nombre_institucion="Asdasd",
        numero_exterior=35
    )
    Empresa.objects.create(
        acerca_de="a",
        calle="Esmeralda",
        codigo_postal=98613,
        colonia="Las joyas",
        latitud=0,
        longitud=0,
        municipio=16,
        numero_exterior=35,
        encargado=usuario_empresa,
        nombre_empresa="horda"
    )
    AreaConocimiento.objects.create(
        nombre="TestArea",
        descripcion="Asdasdasd"
    )
    Categoria.objects.create(
        nombre="Software",
        descripcion="asdasd",
        area_conocimiento=AreaConocimiento.objects.get(nombre="TestArea")
    )
    investigacion = Investigacion.objects.create(
        titulo="Asdasd",
        contenido="asdasdasd"
    )
    investigacion.autores.add(Investigador.objects.get(
        user=User.objects.get(username="usuario_investigador")
    ))
    investigacion.categorias.add(Categoria.objects.get(
        nombre="Software"
    ))
    investigacion.save()
    SolicitudIngreso.objects.create(
        investigador=Investigador.objects.get(user=usuario_investigador),
        institucion_educativa=InstitucionEducativa.objects.get(
            encargado=usuario_institucion
        )
    )


@given(u'que inicio el sistema')
def step_impl(context):
    poblar_base_de_datos()
