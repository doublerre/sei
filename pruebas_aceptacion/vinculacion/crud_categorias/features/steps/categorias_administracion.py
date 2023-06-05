import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from pruebas_aceptacion.features.steps.navegador import navegador


@given(u'que deseo ingresar una nueva categoría como administrador' +
       ' con el usuario "{usuarioC}" y password "{passwordC}"')
def step_impl(context, usuarioC, passwordC):
    driver = navegador.get_navegador()
    driver.get('http://localhost:8000/administracion/categorias/nuevo')
    time.sleep(3)

    # Logeamos como administrador
    usuario = driver.find_element(By.NAME, 'username')
    usuario.send_keys(usuarioC)
    time.sleep(1)
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(passwordC)
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)

    context.driver = driver


@when(u'coloque el nombre "{Nombre_prueba}" el area y la descripación ' +
      '"{descripcion_prueba}" y envíe el formulario')
def step_impl(context, Nombre_prueba, descripcion_prueba):
    # Ingresamos el nombre
    context.driver.find_element(By.NAME, 'nombre').send_keys(Nombre_prueba)
    # Ingresamos el area
    context.driver.find_element(By.XPATH,
                                '/html/body/div/div[2]/section/div/' +
                                'div/div[2]/div/form/' +
                                'div/div/div[2]/div/sel' +
                                'ect/option[2]').click()
    # Ingresamos la descripcion
    context.driver.find_element(
        By.NAME, 'descripcion').send_keys(descripcion_prueba)
    # Enviamos el formulario
    context.driver.find_element(By.XPATH, '/html/body/div/div[2]/section' +
                                '/div/div/div[2]/div/' +
                                'form/div/div/div[4]/button[1]').click()
    time.sleep(2)
    # Buscamos el mensaje de exito
    mensaje = context.driver.find_element(By.XPATH, '/html/body/div/div' +
                                          '[2]/section[1]/div/div[1]/div')
    context.mensaje = mensaje.text


@then(u'se mostrará un mensaje que diga "Categoría registrada correctamente"')
def step_impl(context):
    assert context.mensaje == 'Categoría registrada correctamente'
    context.driver.close()

# pruebas para eliminar una categoria


@given(u'que deseo eliminar la categotía "Prueba" logeo ' +
       'como administrador "{usuarioC}" con la password "{passwordC}"')
def step_impl(context, usuarioC, passwordC):
    driver = navegador.get_navegador()
    driver.get('http://localhost:8000/administracion/categorias/lista')
    time.sleep(3)

    # Logeamos como administrador
    usuario = driver.find_element(By.NAME, 'username')
    usuario.send_keys(usuarioC)
    time.sleep(1)
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(passwordC)
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)

    context.driver = driver


@when(u'presione el botón "eliminar"')
def step_impl(context):
    # precionamos el boton eliminar
    context.driver.find_element(By.XPATH, '/html/body/div/div[2]/section[2]' +
                                '/div/div[2]/div/div[2]/div/' +
                                'table/tbody/tr[5]/td[3]/a[2]').click()
    time.sleep(2)
    # aceptamos la alerta
    context.driver.find_element(By.XPATH, '/html/body/div/div[2]' +
                                '/section/div/div' +
                                '[2]/form/button').click()
    time.sleep(2)
    # Buscamos el mensaje de exito
    mensaje = context.driver.find_element(By.XPATH, '/html/body/div/' +
                                          'div[2]/section[1]/div/div[1]/div')
    context.mensaje = mensaje.text


@then(u'la categoría será removida de la lista.')
def step_impl(context):
    assert context.mensaje == 'Categoría eliminada correctamente'
    context.driver.close()

# pruebas para modificar una categoria


@given(u'que deseo modificar una categoría logeo como administrador ' +
       '"{usuarioC}" con la password "{passwordC}" ' +
       'en la categoria "{id_categoria}"')
def step_impl(context, usuarioC, passwordC, id_categoria):
    driver = navegador.get_navegador()
    driver.get(
        'http://localhost:8000/administracion/categorias/editar/'+id_categoria)
    time.sleep(3)

    # Logeamos como administrador
    usuario = driver.find_element(By.NAME, 'username')
    usuario.send_keys(usuarioC)
    time.sleep(1)
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(passwordC)
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)

    context.driver = driver


@when(u'llene el formulario con el nombre "{Nombre_prueba}" y' +
      ' la descripación "{descripcion_prueba}" y lo envié')
def step_impl(context, Nombre_prueba, descripcion_prueba):
    # Ingresamos el nombre
    context.driver.find_element(By.NAME, 'nombre').send_keys(Nombre_prueba)
    context.driver.find_element(
        By.NAME, 'descripcion').send_keys(descripcion_prueba)
    # Enviamos el formulario
    context.driver.find_element(By.XPATH, '/html/body/div/div[2]/section' +
                                '/div/div/div[2]/div/' +
                                'form/div/div/div[4]/button[1]').click()
    time.sleep(2)
    # Buscamos el mensaje de exito
    mensaje = context.driver.find_element(By.XPATH, '/html/body/div/div' +
                                          '[2]/section[1]/div/div[1]/div')
    context.mensaje = mensaje.text


@then(u'se mostrará el mensaje "{mensaje_exito}"')
def step_impl(context, mensaje_exito):
    assert context.mensaje == mensaje_exito
    context.driver.close()

# pruebas para ver las categorias


@given(u'que deseo mirar las categorías que existen logeo como ' +
       'administrador "{usuarioC}" con la password "{passwordC}"')
def step_impl(context, usuarioC, passwordC):
    driver = navegador.get_navegador()
    driver.get('http://localhost:8000/administracion/categorias/lista')
    time.sleep(3)

    # Logeamos como administrador
    usuario = driver.find_element(By.NAME, 'username')
    usuario.send_keys(usuarioC)
    time.sleep(1)
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(passwordC)
    driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)
    context.driver = driver


@when(u'vaya a la lista en "/administracion/categorias/lista"')
def step_impl(context):
    # Buscamos el titulo
    titulo = context.driver.find_element(
        By.XPATH, '/html/body/div/div[2]/section[1]/div/div[1]/h4')
    context.titulo = titulo.text


@then(u'se mostrara todas las categorías existentes.')
def step_impl(context):
    assert context.titulo == 'Crear nueva categoría'
    context.driver.close()
