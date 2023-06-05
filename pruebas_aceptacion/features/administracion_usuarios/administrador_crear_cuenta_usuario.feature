Característica: Registrar usuario al sistema
	Como administrador del sistema
	Quiero agregar usuarios al sistema
	Para actualizar la lista de usuarios

	Escenario: Creación datos correctos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/usuarios/nuevo"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y relleno el campo de "username" con "GokuFase4" en el formulario
		Y relleno el campo de "password" con "goku1234" en el formulario
		Y relleno el campo de "email" con "super@email.com" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje "Usuario registrado correctamente"

	Escenario: Creación datos incorrectos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/usuarios/nuevo"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y relleno el campo de "username" con "GokuFase4" en el formulario
		Y relleno el campo de "password" con "goku1234" en el formulario
		Y relleno el campo de "email" con "super" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje de error "Introduzca una dirección de correo electrónico válida"
