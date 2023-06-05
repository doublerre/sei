Característica: Consultar empresas
	Como visitante
	Quiero consultar el listado de empresas
	Para ver cuales empresas hay registradas

	Escenario: Consultar empresas
        Dado que existe una empresa llamada "Empresa" con el encargado "encargado"
        Y que ingreso al sistema en el dominio "/empresas"
        Y inicio sesión con el usuario "prueba" y contraseña "prueba"
        Cuando busco la noticia "Empresa"
        Entonces se muestra la empresa llamada "Empresa"

        Escenario: No existen empresas
        Dado que ingreso al sistema en el dominio "/dashboard"
        Y inicio sesión con el usuario "prueba" y contraseña "prueba"
        Cuando hago clic en "usuarios"
        Y hago clic en "empresas"
        Entonces se muestra el mensaje "No existen empresas"