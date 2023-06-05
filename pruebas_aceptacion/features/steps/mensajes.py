from behave import then
from selenium.webdriver.common.by import By


@then(u'se muestra el mensaje de éxito "{mensaje}"')
def step_impl(context, mensaje):
    alerta = context.driver.find_element(By.CLASS_NAME, "alert-success")
    assert alerta.text == mensaje


@then(u'se me muestra el error "{error_texto}"')
def step_impl(context, error_texto):
    lista_errores = context.driver.find_elements(By.CLASS_NAME, "errorlist")

    lis_texts = []

    for lista in lista_errores:
        lis = lista.find_elements(By.TAG_NAME, "li")
        for li in lis:
            lis_texts.append(li.text)

    assert error_texto in lis_texts
