from behave import given, when, then
from selenium.webdriver.common.by import By
import crear_solicitud_helpers as helper


@given(u'que ingreso al sistema en el path "{path}" en su seccion de solicitudes')  # noqa: E501
def step_impl(context, path):  # noqa: F811
    helper.prepare_test_data(context)
    helper.login(context, "Visitante", "test")
    context.driver.get(
        context.get_url(path+str(context.usuario_investigador.pk)))


@given(u'que ingreso al sistema en el path "{path}" en su seccion de solicitudes a mi investigador')  # noqa: E501
def step_impl(context, path):  # noqa: F811
    helper.prepare_test_data(context)
    helper.login(context, "Prueba", "test")
    context.driver.get(
        context.get_url(path+str(context.usuario_investigador.pk)))


@given(u'que ingreso el título y descripción de la solicitud')  # noqa: E501
def step_impl(context):  # noqa: F811
    context.driver.find_element(By.NAME, 'titulo').send_keys("test")
    context.driver.find_element(By.NAME, 'descripcion').send_keys("test")


@when(u'presiono el botón "Guardar"')  # noqa: E501
def step_impl(context):  # noqa: F811
    context.driver.find_element(
        By.XPATH,
        '/html/body/div/div/div/div[2]/div/div/div[2]/form/div/button[1]'
    ).click()


@then(u'se muestra el mensaje "{mensaje}"')  # noqa: E501
def step_impl(context, mensaje):  # noqa: F811
    alertas = context.driver.find_elements(By.CLASS_NAME, 'alert')
    message_found = any(mensaje in alerta.text for alerta in alertas)
    context.driver.close()
    assert message_found
