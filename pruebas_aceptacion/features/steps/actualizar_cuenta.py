from behave import given, then, when
from selenium.webdriver.common.by import By
from time import sleep


@given(u'hago clic en el tipo "{tipo}"')
def step_impl(context, tipo):
    if tipo == "Investigador":
        context.driver.find_element(By.ID, 'investigador').click()
    if tipo == "Empresa":
        context.driver.find_element(By.ID, 'empresa').click()
    if tipo == "Institución Educativa":
        context.driver.find_element(By.ID, 'institucion-educativa').click()


@when(u'envío la solicitud presionando el botón de Guardar')
def step_impl(context):
    context.driver.execute_script("window.scrollTo(0, 1000)")
    sleep(1)
    context.driver.find_element(By.CLASS_NAME, "btn-primary").click()
    sleep(1)


@then(u'se me indica que mi solicitud fue enviada')
def step_impl(context):
    titulo = context.driver.find_element(By.CLASS_NAME, "titulo-seccion").text
    actual = "Sus datos están en espera de ser aprobados por un administrador"

    assert titulo == actual
