import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from pruebas_aceptacion.features.steps.navegador import navegador


@given(u'que tengo una solicitud de trabajo e ingrso a "{link}" ' +
       'con el usuario "{usuarioC}" y la password "{passwordC}"')
def step_impl(context, link, usuarioC, passwordC):
    driver = navegador.get_navegador()
    driver.get('http://127.0.0.1:8000/usuarios/login')
    time.sleep(3)

    # Logeamos como administrador
    usuario = driver.find_element(By.NAME, 'username')
    usuario.send_keys(usuarioC)
    time.sleep(1)
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(passwordC)
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(3)

    # Vamos al link
    driver.get('http://127.0.0.1:8000'+link)
    context.driver = driver


@when(u'hago clic en el boton "{boton}"')
def step_impl(context, boton):
    driver = context.driver
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div' +
                        '/div/div[1]/table/tbody/tr[1]' +
                        '/td[3]/button').click()
    time.sleep(2)

    if boton == "aceptar":
        # Aceptamos la solicitud
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/' +
                            'div/div/div[1]/table/tbody/tr[1]/td[3]' +
                            '/div/div/div/div[3]/a[1]/span').click()
        time.sleep(2)
    elif boton == "Rechazar":
        # Cancelamos la solicitud
        driver.find_element(By.XPATH, '/html/body/div[1]/div/' +
                            'div/div[3]/div/div/div[1]' +
                            '/table/tbody/tr/td[3]/div/div' +
                            '/div/div[3]/a[2]/span').click()
        time.sleep(2)

    # Checamos el estado de la solicitud
    if boton == "aceptar":
        driver.get('http://127.0.0.1:8000/perfil/trabajos')
        time.sleep(2)
        # Obtenemos el estado de la solicitud
        estado = driver.find_element(By.XPATH, '/html/body/div/' +
                                     'div/div/div[3]/div/div/div[1]' +
                                     '/table/tbody/tr[1]/td[3]')
        context.estado = estado.text
    elif boton == "Rechazar":
        driver.get('http://127.0.0.1:8000/perfil/trabajos/historial')
        time.sleep(2)
        # Obtenemos el estado de la solicitud
        estado = driver.find_element(By.XPATH, '/html/body/div/div/' +
                                     'div/div[3]/div/div/div[1]' +
                                     '/table/tbody/tr[1]/td[3]')
        context.estado = estado.text
    driver.close()


@then(u'el estado de la solicitud cambia a "{estado}"')
def step_impl(context, estado):
    assert context.estado == estado
