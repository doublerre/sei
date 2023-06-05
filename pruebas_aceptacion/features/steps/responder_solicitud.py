from behave import given, when
from selenium.webdriver.common.by import By
from investigadores.models import SolicitudTrabajo
import crear_solicitud_helpers as helper


@given(u'que tengo una solicitud de trabajo')  # noqa: E501
def step_impl(context):  # noqa: F811
    helper.prepare_test_data(context)
    context.solicitud_trabajo = SolicitudTrabajo.objects.create(
        descripcion="Solicitud de ejemplo",
        titulo="Solicitud",
        usuario_a_vincular=context.investigador,
        usuario_solicitante=context.usuario_visitante,
        estado="E",
    )


@given(u'que ingreso al sistema en el path "{path}" en su seccion de solicitudes a responder')  # noqa: E501
def step_impl(context, path):  # noqa: F811
    helper.login(context, "Prueba", "test")
    context.driver.get(
        context.get_url(path)
    )


@when(u'presiono el botón "{boton_text}"')  # noqa: E501
def step_impl(context, boton_text):  # noqa: F811
    boton = context.driver.find_element(
        By.CLASS_NAME,
        'btn-outline-success'
    )
    boton.click()
    contenedor = boton.find_element(
        By.XPATH,
        './..'
    )
    contenedor.find_element(
        By.LINK_TEXT,
        boton_text
    ).click()
