Característica: Eliminar perfil
	Como usuario
	Quiero eliminar mi perfil
	Para retirar mis datos del sistema

	Escenario: Eliminación correcta
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/perfil/eliminar"
		Y inicio mi sesión con el usuario "usuario_investigador" y contraseña "password1234"
        Cuando confirmo mi decisión
		Entonces se muestra el mensaje "Cuenta eliminada correctamente"
