from behave import then, when
from selenium.webdriver.common.by import By


@when(u'hago clic en Crear cuenta')
def step_impl(context):
    context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/form/button").click()


@then(u'puedo ver mi nombre de usuario "{usuario}" en la página principal')
def step_impl(context, usuario):
    mensaje = context.driver.find_element(
        By.XPATH, "/html/body/div/div/div[1]/div/div[2]").text
    print(mensaje)
    assert mensaje == f"{usuario} se registró de manera exitosa"
