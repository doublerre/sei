Característica: Registrar investigador al sistema
	Como administrador del sistema
	Quiero agregar investigadores al sistema
	Para actualizar la lista de investigadores

	Escenario: Creación datos correctos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/investigadores/nuevo"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y elijo "root" en el campo de "user" en el formulario
		Y elijo "Nivel 1" en el campo de "nivel" en el formulario
		Y relleno el campo de "curp" con "BEGE010204HZSLNLA5" en el formulario
		Y relleno el campo de "codigo_postal" con "98613" en el formulario
		Y elijo "Guadalupe" en el campo de "municipio" en el formulario
		Y relleno el campo de "colonia" con "Las joyas" en el formulario
		Y relleno el campo de "calle" con "Esmeralda" en el formulario
		Y relleno el campo de "numero_exterior" con "35" en el formulario
		Y relleno el campo de "acerca_de" con "asd" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje "Investigador registrado correctamente"

	Escenario: Creación datos incorrectos
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/investigadores/nuevo"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Y elijo "root" en el campo de "user" en el formulario
		Y elijo "Nivel 1" en el campo de "nivel" en el formulario
		Y relleno el campo de "curp" con "BEGE010204HZSLNLA5" en el formulario
		Y relleno el campo de "codigo_postal" con "54321" en el formulario
		Y elijo "Jerez" en el campo de "municipio" en el formulario
		Y relleno el campo de "colonia" con "Torreslocas" en el formulario
		Y relleno el campo de "calle" con "Esmeralda" en el formulario
		Y relleno el campo de "numero_exterior" con "35" en el formulario
		Y relleno el campo de "acerca_de" con "asd" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
		Entonces se muestra el mensaje de error "Error al obtener los datos de ubicación"
