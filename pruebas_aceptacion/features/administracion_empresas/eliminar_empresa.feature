Característica: Eliminar una empresa
	Como administrador
	Quiero eliminar una empresa
	Para que ya no se muestre en el listado de empresas

	Escenario: Eliminación exitosa
        Dado que existe una empresa llamada "Empresa" con el encargado "encargado"
        Y que ingreso al sistema en el dominio "/administracion/empresas/lista"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y busco el registro de "Empresa"
        Cuando hago clic en la opción "eliminar"
        Y confirmo mi decisión
        Y me redirijo a la ruta "/administracion/empresas/lista"
        Entonces no se encuentra el registro de "Empresa"