Característica: Responder solicitud
	Como Investigador
	Quiero contestar una solicitud de trabajo
	Para decidir si darle seguimiento o rechazarla

	Escenario: Solicitud aceptada
		Dado que tengo una solicitud de trabajo
		Y que ingreso al sistema en el path "/perfil/solicitudes_trabajo" en su seccion de solicitudes a responder
		Cuando presiono el botón "Aceptar"
		Entonces se muestra el mensaje "La solicitud ha sido aceptada"

	Escenario: Solicitud rechazada
		Dado que tengo una solicitud de trabajo
		Y que ingreso al sistema en el path "/perfil/solicitudes_trabajo" en su seccion de solicitudes a responder
		Cuando presiono el botón "Rechazar"
		Entonces se muestra el mensaje "La solicitud ha sido rechazada"
