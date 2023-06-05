Característica: Actualizar perfil como institución
	Como institución
	Quiero actualizar los datos de mi cuenta
	Para mantener actualizada mi información en el sistema

	Escenario: Datos correctos
        Dado que ingreso al sistema en el dominio "/usuarios/login"
        Y inicio sesión como institución con el usuario "usuario-institucion" y contraseña "prueba"
        Y hago clic en "perfil"
        Y hago clic en "actualizar"
        Y relleno el campo de "acerca de" con "Soy un crack" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se muestra el mensaje de éxito "Perfil actualizado correctamente"

        Escenario: Datos incorrectos
        Dado que ingreso al sistema en el dominio "/usuarios/login"
        Y inicio sesión como institución con el usuario "usuario-institucion" y contraseña "prueba"
        Y hago clic en "perfil"
        Y hago clic en "actualizar"
        Y relleno el campo de "acerca de" con " " en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se me muestra el error "Este campo es obligatorio."