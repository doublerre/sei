from behave import when
from selenium.webdriver.common.by import By


@when(u'respondo a la solicitud como "{}"')
def step_impl(context, respuesta):
    context.driver.find_element(By.LINK_TEXT, respuesta).click()
