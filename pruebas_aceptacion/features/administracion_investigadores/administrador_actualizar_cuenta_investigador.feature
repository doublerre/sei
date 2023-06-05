Característica: Actualizar investigador
	Como administrador del sistema
	Quiero actualizar la información de un investigador
	Para actualizar la lista de investigadores

	Escenario: Actualizar datos correctos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/investigadores/editar/" para el investigador "usuario_investigador"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y relleno el campo de "acerca_de" con "Esto es lo mejor" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje "Investigador actualizado correctamente"

	Escenario: Actualizar datos incorrectos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/investigadores/editar/" para el investigador "usuario_investigador"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y relleno el campo de "colonia" con "Torreslocas" en el formulario
		Y relleno el campo de "codigo_postal" con "66666" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje de error "Error al obtener los datos de ubicación"
