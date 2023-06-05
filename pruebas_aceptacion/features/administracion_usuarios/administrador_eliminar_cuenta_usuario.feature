Característica: Eliminar usuario
	Como administrador del sistema
	Quiero eliminar a un usuario del sistema
	Para mantener orden en el sistema

	Escenario: Eliminación correcta
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/usuarios/eliminar/" para el usuario "usuario_visitante"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Cuando confirmo mi decisión
		Entonces se muestra el mensaje "Usuario eliminado correctamente"
