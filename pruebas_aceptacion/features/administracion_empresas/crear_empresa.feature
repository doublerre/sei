Característica: Agregar una empresa
	Como administrador
	Quiero crear una empresa
	Para que los usuarios puedan consultarla

	Escenario: Datos correctos al crear empresa
        Dado que ingreso al sistema en el dominio "/usuarios/login"
        Y dado que existe la categoría "Software" del área "Ingeniería"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y hago clic en "perfil"
        Y hago clic en "tablas"
        Y hago clic en "empresas"
        Y hago clic en "crear"
        Y elijo "root" en el campo de "encargado" en el formulario
        Y relleno el campo de "nombre empresa" con "Empresa" en el formulario
        Y elijo "Software" en el campo de "especialidades" en el formulario
        Y relleno el campo de "codigo postal" con "99390" en el formulario
        Y elijo "Jerez" en el campo de "municipio" en el formulario
        Y relleno el campo de "colonia" con "Alamitos" en el formulario
        Y relleno el campo de "calle" con "Mezquite" en el formulario
        Y relleno el campo de "numero exterior" con "29" en el formulario
        Y relleno el campo de "acerca de" con "Somos una empresa de software" en el formulario
        Y relleno el campo de "imagen" con "/tmp/noticia.png" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se muestra el mensaje de éxito "Empresa registrada correctamente"

        Escenario: Datos incorrectos al crear empresa
        Dado que ingreso al sistema en el dominio "/administracion/empresas/nuevo"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se me pide que rellene correctamente el campo de "encargado"