import navegador
from selenium.webdriver.common.by import By
from investigadores.models import (
    Investigador,
    NivelInvestigador)
from usuarios.models import User, TipoUsuario


def prepare_test_data(context):
    context.driver = navegador.get_navegador()
    context.tipo_investigador = TipoUsuario.objects.create(
        tipo="Investigador")
    context.usuario_investigador = User.objects.create(
        username="Prueba",
        email="asd@asd.com",
        is_active=True,
        tipo_usuario=context.tipo_investigador,
        aprobado=True)
    context.usuario_investigador.set_password("test")
    context.usuario_investigador.save()
    context.usuario_visitante = User.objects.create(
        username="Visitante",
        email="inv@inv.com",
        is_active=True)
    context.usuario_visitante.set_password("test")
    context.usuario_visitante.save()
    context.nivel_1 = NivelInvestigador.objects.create(
        nivel=1,
        descripcion="lorem"
    )
    context.investigador = Investigador.objects.create(
        nivel=context.nivel_1,
        user=context.usuario_investigador,
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


def login(context, username, password):
    context.driver.get(context.get_url("/usuarios/login"))
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    context.driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[1]/div/form/button').click()
