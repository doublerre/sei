from behave import when, given
from selenium.webdriver.common.by import By
from time import sleep


@given(u'hago clic en "{boton}"')
def step_impl(context, boton):
    sleep(2)
    context.driver.find_element(By.NAME, boton).click()


@given(u'hago clic en la opción "{boton}"')
def step_impl(context, boton):
    boton = boton.replace(" ", "-")
    opcion = context.boton.find_element(By.ID, boton)
    context.driver.execute_script("arguments[0].click();", opcion)


@when(u'hago clic en la opción "{boton}"')
def step_impl(context, boton):
    boton = boton.replace(" ", "-")
    opcion = context.boton.find_element(By.ID, boton)
    context.driver.execute_script("arguments[0].click();", opcion)
    sleep(0.1)


@when(u'confirmo mi decisión')
def step_impl(context):
    context.driver.find_element(By.NAME, "confirmar").click()


@when(u'hago clic en "{boton}"')
def step_impl(context, boton):
    btn = context.driver.find_element(By.NAME, boton)
    context.driver.execute_script("arguments[0].click();", btn)
