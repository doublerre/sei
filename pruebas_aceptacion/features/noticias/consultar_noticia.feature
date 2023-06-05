Característica: Consultar una noticia
	Como visitante
	Quiero consultar una noticia
	Para ver el contenido de la noticia

	Escenario: Consultar noticia
        Dado que existe una noticia llamada "Noticia"
        Y que ingreso al sistema en el dominio "/noticias"
        Y inicio sesión con el usuario "prueba" y contraseña "prueba"
        Y busco la noticia "Noticia"
        Cuando hago clic en la opción "leer mas"
        Entonces se muestra la noticia con el título "Noticia"

        Escenario: No existen noticias
        Dado que ingreso al sistema en el dominio "/dashboard"
        Y inicio sesión con el usuario "prueba" y contraseña "prueba"
        Cuando hago clic en "noticias"
        Entonces se muestra el mensaje "No existen noticias"