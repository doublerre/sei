Característica: Actualizar usuario
	Como administrador del sistema
	Quiero actualizar la información de un usuario
	Para actualizar la lista de usuarios

	Escenario: Actualizar datos correctos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/usuarios/editar/" para el usuario "usuario_visitante"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y relleno el campo de "password" con "goku1234" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje "Usuario actualizado correctamente"

	Escenario: Actualizar datos incorrectos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/usuarios/editar/" para el usuario "usuario_visitante"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y relleno el campo de "password" con "goku1234" en el formulario
		Y relleno el campo de "email" con "goku" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje de error "Introduzca una dirección de correo electrónico válida."
