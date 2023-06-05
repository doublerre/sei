Característica: Rechazar solicitud correctamente
    Yo como investigador quiero poder rechazar 
    cualquier solicitud de trabajo para hacer 
    solo las que yo quiera.

    Escenario: Rechazar solicitud correctamente
    Dado que tengo una solicitud de trabajo e ingrso a "/perfil/solicitudes_trabajo" con el usuario "Guzman" y la password "admin"
    Cuando hago clic en el boton "Rechazar"
    Entonces el estado de la solicitud cambia a "Rechazado"