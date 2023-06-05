Característica: Buscar en mapa
	Como usuario
	Quiero buscar investigadores/empresas/instituciones educativas
	Para poder contactar con ellos

	Escenario: Búsqueda correcta
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/dashboard"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
		Cuando selecciono la categoría "Software"
		Entonces se muestran los investigadores/empresas/instituciones educativas que tengan conocimiento de esa categoría

