from behave import then, given
from selenium.webdriver.common.by import By


@given(u'busco la noticia "{titulo}"')
def step_impl(context, titulo):
    noticias = context.driver.find_elements(By.CLASS_NAME, "noticia")

    for n in noticias:
        titulo_texto = n.find_element(By.CLASS_NAME, "card-title").text
        if titulo_texto == titulo:
            context.boton = n.find_element(By.CLASS_NAME, "list-group")
            break


@then(u'se muestra la noticia con el título "{titulo}"')
def step_impl(context, titulo):
    titulo_texto = context.driver.find_element(
        By.CLASS_NAME, "card-title").text

    assert titulo == titulo_texto
