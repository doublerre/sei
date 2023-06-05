from behave import given
from helpers.usuarios_helpers import crear_tipo_usuario, crear_usuario
from helpers.instituciones_educativas_helpers import (
    crear_institucion_educativa)
from helpers.vinculacion_helpers import (
    crear_area_conocimiento, crear_categoria, crear_noticia)
from helpers.investigadores_helpers import (
    crear_nivel_investigador, crear_investigador)
from helpers.empresas_helpers import crear_empresa


@given(u'dado que existe la categoría "{categoria_nombre}" del área "{area_nombre}')
def step_impl(context, categoria_nombre, area_nombre):
    context.area = crear_area_conocimiento(area_nombre, "area")
    context.categoria = crear_categoria(
        categoria_nombre, context.area, "categoria")


@given(u'que existe una empresa llamada "{nombre_empresa}" con el encargado "{encargado}"')
def step_impl(context, nombre_empresa, encargado):
    area_conocimiento = crear_area_conocimiento(
        "Ingeniería", "Sobre ingeniería")
    categoria = crear_categoria(
        "Software", area_conocimiento, "Sobre software")
    tipo_empresa = crear_tipo_usuario("Empresa")
    usuario_encargado = crear_usuario(
        usuario=encargado,
        correo="encargado@encargado.com",
        contra="12345678",
        tipo=tipo_empresa,
        aprobado=True
    )
    context.empresa = crear_empresa(
        encargado=usuario_encargado,
        nombre_empresa=nombre_empresa,
        codigo_postal='99390',
        municipio=19,
        especialidades=[categoria],
        colonia='Alamitos',
        calle='Mezquite',
        numero_exterior='29',
        acerca_de='Info',
        imagen="/tmp/noticia.png"
    )


@given(u'que existe una noticia llamada "{titulo_noticia}"')
def step_impl(context, titulo_noticia):
    escritor = crear_usuario(
        "escritor", "escritor@escritor.com", "12345678")
    context.noticia = crear_noticia(
        titulo_noticia, "Contenido", escritor, "/noticias/noticia.png")


@given(u'que existe una solicitud de una institución educativa llamada "{nombre_institucion}"')
def step_impl(context, nombre_institucion):
    context.tipo_institucion = crear_tipo_usuario("Institucion")
    context.tipo_investigador = crear_tipo_usuario("Investigador")
    context.usuario_institucion = crear_usuario(
        nombre_institucion, "prueba-institucion@prueba.com",
        "prueba", context.tipo_institucion)
    context.usuario_investigador = crear_usuario(
        "Investigador", "prueba-investigador@prueba.com",
        "prueba", context.tipo_investigador)
    context.area_conocimiento = crear_area_conocimiento(
        "Ingeniería", "Sobre ingeniería")
    context.categoria = crear_categoria(
        "Software", context.area_conocimiento, "Sobre software")
    context.nivel_1 = crear_nivel_investigador(1, "Nivel 1")
    context.investigador = crear_investigador(
        usuario=context.usuario_investigador,
        nivel=context.nivel_1,
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
    context.institucion_educativa = crear_institucion_educativa(
        encargado=context.usuario_institucion,
        nombre_institucion="Institución Prueba",
        especialidades=[context.categoria],
        latitud=0,
        longitud=0,
        miembros=[context.investigador],
        codigo_postal=99390,
        municipio=20,
        colonia="Alamitos",
        calle="Mezquite",
        numero_exterior=29,
        acerca_de="Soy una institución"
    )
