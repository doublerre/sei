Característica: Ediar una empresa
	Como administrador
	Quiero editar una empresa
	Para actualizar su información

	Escenario: Datos correctos al editar empresa
        Dado que existe una empresa llamada "Empresa" con el encargado "encargado"
        Y que ingreso al sistema en el dominio "/usuarios/login"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y hago clic en "perfil"
        Y hago clic en "tablas"
        Y hago clic en "empresas"
        Y busco el registro de "Empresa"
        Y hago clic en la opción "editar"
        Y relleno el campo de "acerca de" con "Somos una super empresa" en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se muestra el mensaje de éxito "Empresa actualizada correctamente"

        Escenario: Datos incorrectos al editar empresa
        Dado que existe una empresa llamada "Empresa" con el encargado "encargado"
        Y que ingreso al sistema en el dominio "/administracion/empresas/lista"
        Y inicio sesión como administrador con el usuario "root" y contraseña "prueba"
        Y busco el registro de "Empresa"
        Y hago clic en la opción "editar"
        Y relleno el campo de "acerca de" con " " en el formulario
        Cuando envío la solicitud presionando el botón de Guardar
        Entonces se me indica que el campo de "acerca de" es obligatorio