Característica: Eliminar investigador
	Como administrador del sistema
	Quiero eliminar a un investigador del sistema
	Para mantener orden en el sistema

	Escenario: Eliminación correcta
		Dado que inicio el sistema
		Y que ingreso al sistema en el dominio "/administracion/investigadores/eliminar/" para el investigador "usuario_investigador"
		Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Cuando confirmo mi decisión
		Entonces se muestra el mensaje "Investigador eliminado correctamente"
