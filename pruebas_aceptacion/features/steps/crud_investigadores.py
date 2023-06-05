from behave import given
from investigadores.models import Investigador
import navegador


@given(u'que ingreso al sistema en el dominio "{url}" para el investigador "{username}"')
def step_impl(context, url, username):
    context.driver = navegador.get_navegador()
    context.driver.get(
        context.get_url(
            url +
            str(Investigador.objects.get(user__username=username).pk)))
    context.driver.maximize_window()
