def after_scenario(context, scenario):
    try:
        if context.driver:
            context.driver.close()
    except Exception:
        pass
