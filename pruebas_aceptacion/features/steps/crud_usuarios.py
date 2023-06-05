from behave import given
from usuarios.models import User
import navegador


@given(u'que ingreso al sistema en el dominio "{url}" para el usuario "{username}"')
def step_impl(context, url, username):
    context.driver = navegador.get_navegador()
    context.driver.get(
        context.get_url(
            url +
            str(User.objects.get(username=username).pk)))
    context.driver.maximize_window()
