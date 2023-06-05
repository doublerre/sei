from behave import given
from selenium.webdriver.common.by import By
from helpers.usuarios_helpers import crear_usuario, crear_tipo_usuario
from helpers.investigadores_helpers import (
    crear_investigador, crear_nivel_investigador)
from helpers.instituciones_educativas_helpers import (
    crear_institucion_educativa)
from helpers.vinculacion_helpers import (
    crear_area_conocimiento, crear_categoria)
from helpers.empresas_helpers import crear_empresa


@given(u'inicio sesión como empresa con el usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    area_conocimiento = crear_area_conocimiento(
        "Ingeniería", "Sobre ingeniería")
    categoria = crear_categoria(
        "Software", area_conocimiento, "Sobre software")
    tipo_empresa = crear_tipo_usuario("Empresa")
    usuario_encargado = crear_usuario(
        usuario=usuario,
        correo="encargado@encargado.com",
        contra=contra,
        tipo=tipo_empresa,
        aprobado=True
    )
    context.empresa = crear_empresa(
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
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()


@given(u'inicio sesión como institución con el usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    context.tipo_institucion = crear_tipo_usuario("Institucion Educativa")
    context.tipo_investigador = crear_tipo_usuario("Investigador")
    context.usuario_institucion = crear_usuario(
        usuario, "prueba-institucion@prueba.com",
        contra, context.tipo_institucion, aprobado=True)
    context.usuario_investigador = crear_usuario(
        "Investigador", "prueba-investigador@prueba.com",
        "prueba", context.tipo_investigador, aprobado=True)
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
        municipio=19,
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
        municipio=19,
        colonia="Alamitos",
        calle="Mezquite",
        numero_exterior=29,
        acerca_de="Soy una institución"
    )
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()


@given(u'inicio sesión como investigador con el usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    context.tipo_investigador = crear_tipo_usuario("Investigador")
    context.usuario_investigador = crear_usuario(
        usuario=usuario, correo="prueba@prueba.com",
        contra=contra, tipo=context.tipo_investigador, aprobado=True)
    context.nivel_1 = crear_nivel_investigador(1, "Nivel 1")
    context.investigador = crear_investigador(
        usuario=context.usuario_investigador,
        nivel=context.nivel_1,
        curp="AUCJ011020HZSGRVA1",
        codigo_postal=99390,
        municipio=19,
        colonia="Alamitos",
        calle="Mezquite",
        numero_exterior=29,
        acerca_de="Soy un investigador"
    )
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()


@given(u'inicio sesión con el usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    crear_usuario(usuario=usuario, correo="prueba@prueba.com", contra=contra)
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()


@given(u'inicio mi sesión con el usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()


@given(u'inicio sesión como administrador con el usuario "{usuario}" y contraseña "{contra}"')
def step_impl(context, usuario, contra):
    crear_usuario(usuario=usuario, correo="root@root.com",
                  contra=contra, superusuario=True, staff=True)
    context.driver.find_element(By.NAME, 'username').send_keys(usuario)
    context.driver.find_element(By.NAME, 'password').send_keys(contra)
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()
