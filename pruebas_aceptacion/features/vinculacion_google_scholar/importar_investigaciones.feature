Característica: Importar investigaciones desde Google Scholar
    Yo como investigador
    Quiero importar mis investigaciones de Google Scholar a el sistema
    Para que la información de éstas se almacene en mi perfil

    Escenario: Importación exitosa
    Dado que ingreso al sistema en el dominio "/usuarios/login"
    Y inicio sesión como investigador con el usuario "usuario-investigador" y contraseña "prueba"
    Y hago clic en "perfil"
    Y hago clic en "investigaciones"
    Y relleno el campo de "profile-url" con "https://scholar.google.com/citations?hl=en&user=YGnk7uoAAAAJ" en el formulario
    Cuando hago clic en "cargar"
    Entonces se muestra el mensaje de éxito "Carga de investigaciones exitosa"

    Escenario: Perfil inexistente
    Dado que ingreso al sistema en el dominio "/usuarios/login"
    Y inicio sesión como investigador con el usuario "usuario-investigador" y contraseña "prueba"
    Y hago clic en "perfil"
    Y hago clic en "investigaciones"
    Y relleno el campo de "profile-url" con "perfil_inexistente" en el formulario
    Cuando hago clic en "cargar"
    Entonces se muestra el mensaje "No se encontró el perfil de google scholar"