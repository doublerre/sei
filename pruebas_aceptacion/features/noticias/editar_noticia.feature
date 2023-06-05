Característica: Ediar una noticia
	Como administrador
	Quiero editar una noticia
	Para actualizar su información

	Escenario: Datos correctos al editar noticia
        Dado que existe una noticia llamada "Noticia"
        Y que ingreso al sistema en el dominio "/usuarios/login"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y hago clic en "perfil"
        Y hago clic en "tablas"
        Y hago clic en "noticias"
        Y busco el registro de "Noticia"
        Y hago clic en la opción "editar"
        Y relleno el campo de "titulo" con "Noticia modificada" en el formulario
        Y relleno el campo de "contenido" con "Contenido modificado" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se muestra el mensaje de éxito "Noticia actualizada correctamente"

        Escenario: Datos incorrectos al editar noticia
        Dado que existe una noticia llamada "Noticia"
        Y que ingreso al sistema en el dominio "/administracion/noticias/lista"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y busco el registro de "Noticia"
        Y hago clic en la opción "editar"
        Y relleno el campo de "titulo" con " " en el formulario
        Y relleno el campo de "contenido" con " " en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se me indica que el campo de "titulo" es obligatorio