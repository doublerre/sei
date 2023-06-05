from behave import when, then
from investigadores.models import Investigador
from selenium.webdriver.common.by import By


@when(u'selecciono la categoría "Software"')
def step_impl(context):
    menus = context.driver.find_elements(By.CLASS_NAME, 'choices__inner')
    menus[1].click()
    context.driver.find_element(
        By.ID,
        'choices--sugerencias-item-choice-1').click()


@then(u'se muestran los investigadores/empresas/instituciones educativas que tengan conocimiento de esa categoría')
def step_impl(context):
    assert len(context.driver.find_elements(
        By.CLASS_NAME,
        'leaflet-marker-icon'
    )) == Investigador.objects.count()
