Característica: Creación de solicitud
	Como usuario
	Quiero hacer una solicitud de trabajo a un investigador
	Para resolver un problema con la ayuda de un experto

	Escenario: Datos correctos
		Dado que ingreso al sistema en el path "/formularios/solicitud_trabajo/" en su seccion de solicitudes
		Y que ingreso el título y descripción de la solicitud
		Cuando presiono el botón "Guardar"
		Entonces se muestra el mensaje "Solicitud de trabajo a el investigador"
	
	Escenario: Auto solicitud
		Dado que ingreso al sistema en el path "/formularios/solicitud_trabajo/" en su seccion de solicitudes a mi investigador
		Y que ingreso el título y descripción de la solicitud
		Cuando presiono el botón "Guardar"
		Entonces se muestra el mensaje "Un investigador no puede hacer una solicitud a sí mismo"
