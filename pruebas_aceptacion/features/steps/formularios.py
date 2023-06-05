from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


@given(u'relleno el campo de "{nombre_campo}" con "{valor}" en el formulario')
def step_impl(context, nombre_campo, valor):
    nombre_campo = nombre_campo.replace(" ", "_")
    campo = context.driver.find_element(By.NAME, nombre_campo)
    campo.clear()
    campo.send_keys(valor)


@given(u'elijo "{opcion}" en el campo de "{campo}" en el formulario')
def step_impl(context, opcion, campo):
    selects = context.driver.find_elements(By.CLASS_NAME, "form-select")
    for select in selects:
        if select.get_attribute("name") == campo:
            select = Select(select)
            select.select_by_visible_text(opcion)
            break


@then(u'se me pide que rellene correctamente el campo de "{campo}"')
def step_impl(context, campo):
    campo = campo.replace(" ", "_")
    campoEncontrado = context.driver.find_element(By.NAME, campo)
    assert campoEncontrado == context.driver.switch_to.active_element


@then(u'se me indica que el campo de "{campo}" es obligatorio')
def step_impl(context, campo):
    campo = campo.replace(" ", "_")
    campoEncontrado = context.driver.find_element(By.NAME, campo)
    assert "is-invalid" in campoEncontrado.get_attribute('class').split()


@then(u'se me muestra el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    errores = context.driver.find_element(By.CLASS_NAME, "errorlist")
    errores = errores.find_elements(By.TAG_NAME, "li")

    texto_errores = []

    for error in errores:
        texto_errores.append(error.text)

    assert mensaje in texto_errores


@then(u'se muestra el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    errores = context.driver.find_elements(By.CLASS_NAME, "alert-danger")

    texto_errores = []

    for error in errores:
        texto_errores.append(error.text)

    assert mensaje in "".join(texto_errores)


@then(u'se me muestra la notificación de error "{mensaje}"')
def step_impl(context, mensaje):
    notificacion = context.driver.find_element(
        By.CLASS_NAME, "notificador").find_element(By.TAG_NAME, "div")
    assert notificacion.text == mensaje
