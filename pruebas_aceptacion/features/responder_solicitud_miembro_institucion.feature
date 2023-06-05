Característica: Responder solicitud miembro
	Como institución educativa
	Quiero responder a la solicitud de un investigador a mi lista de miembros
	Para mantener el control de mi lista de miembros

	Escenario: Solicitud aceptada
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/institucion_educativa/solicitud_ingreso"
		Y inicio mi sesión con el usuario "usuario_institucion" y contraseña "password1234"
        Cuando respondo a la solicitud como "Aceptar"
		Entonces se muestra el mensaje "Se ha aceptado la solicitud del investigador"

	Escenario: Solicitud rechazada
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/institucion_educativa/solicitud_ingreso"
		Y inicio mi sesión con el usuario "usuario_institucion" y contraseña "password1234"
        Cuando respondo a la solicitud como "Negar"
		Entonces se muestra el mensaje "Se ha rechazado la solicitud del investigador"
