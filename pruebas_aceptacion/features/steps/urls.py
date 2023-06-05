from behave import given, when
import navegador


@given(u'que ingreso al sistema en el dominio "{url}"')
def step_impl(context, url):
    context.driver = navegador.get_navegador()
    context.driver.get(context.get_url(url))
    context.driver.maximize_window()


@when(u'me redirijo a la ruta "{url}"')
def step_impl(context, url):
    context.driver.get(context.get_url(url))
    context.driver.maximize_window()
