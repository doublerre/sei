from behave import when, then
from selenium.webdriver.common.by import By


@when(u'busco la noticia "{nombre_empresa}"')
def step_impl(context, nombre_empresa):
    empresas = context.driver.find_elements(By.CLASS_NAME, "empresa")

    for e in empresas:
        nombre_texto = e.find_element(By.CLASS_NAME, "card-title").text
        if nombre_texto == nombre_empresa:
            context.nombre_texto = nombre_texto


@then(u'se muestra la empresa llamada "{nombre_empresa}"')
def step_impl(context, nombre_empresa):
    assert context.nombre_texto == nombre_empresa
