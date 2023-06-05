Característica: Responder solicitud de una institución educativa
	Como administrador
	Quiero reponder la solicitud de una institución educativa
	Para que se genere su perfil o se elimine su solicitud

	Escenario: Aprobar solicitud
        Dado que inicio el sistema
        Y que ingreso al sistema en el dominio "/administracion/empresas/solicitud"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y busco el registro de "usuario_empresa"
        Cuando hago clic en la opción "aprobar"
        Entonces se muestra el mensaje "Solicitud aceptada"
	
	Escenario: Rechazar solicitud
        Dado que inicio el sistema
        Y que ingreso al sistema en el dominio "/administracion/empresas/solicitud"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y busco el registro de "usuario_empresa"
        Cuando hago clic en la opción "rechazar"
        Y confirmo mi decisión
        Entonces se muestra el mensaje "Empresa eliminada correctamente"
