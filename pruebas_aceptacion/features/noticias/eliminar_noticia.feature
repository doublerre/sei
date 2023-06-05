Característica: Eliminar una notiica
	Como administrador
	Quiero eliminar una noticia
	Para que ya no se muestre en el listado de noticias

	Escenario: Eliminación exitosa
        Dado que existe una noticia llamada "Noticia"
        Y que ingreso al sistema en el dominio "/administracion/noticias/lista"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y busco el registro de "Noticia"
        Cuando hago clic en la opción "eliminar"
        Y confirmo mi decisión
        Y me redirijo a la ruta "/administracion/noticias/lista"
        Entonces no se encuentra el registro de "Noticia"