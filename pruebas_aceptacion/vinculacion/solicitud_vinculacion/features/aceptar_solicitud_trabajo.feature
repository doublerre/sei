Característica: Aceptar solicitud de trabajo
    Yo como investigador quiero poder aceptar cualquier 
    solicitud de trabajo para comenzar nuevos trabajos 
    cuando lo requiera

    Escenario: Aceptar solicitud correctamente
    Dado que tengo una solicitud de trabajo e ingrso a "/perfil/solicitudes_trabajo" con el usuario "Guzman" y la password "admin"
    Cuando hago clic en el boton "aceptar"
    Entonces el estado de la solicitud cambia a "Aceptado"