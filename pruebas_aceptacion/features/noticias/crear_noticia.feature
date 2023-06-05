Característica: Agregar una noticia
	Como administrador
	Quiero crear una noticia
	Para que los usuarios puedan consultarla

	Escenario: Datos correctos al crear noticia
        Dado que ingreso al sistema en el dominio "/usuarios/login"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y hago clic en "perfil"
        Y hago clic en "tablas"
        Y hago clic en "noticias"
        Y hago clic en "crear"
        Y relleno el campo de "titulo" con "Noticia 1" en el formulario
        Y relleno el campo de "contenido" con "Contenido noticia 1" en el formulario
        Y elijo "root" en el campo de "escritor" en el formulario
        Y relleno el campo de "imagen" con "/tmp/noticia.png" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se muestra el mensaje de éxito "Noticia registrada correctamente"

        Escenario: Datos incorrectos al crear noticia
        Dado que ingreso al sistema en el dominio "/administracion/noticias/nuevo"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se me pide que rellene correctamente el campo de "titulo"