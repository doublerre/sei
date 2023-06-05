from instituciones_educativas.models import InstitucionEducativa


def crear_institucion_educativa(encargado, nombre_institucion, especialidades,
                                miembros, codigo_postal, municipio, colonia,
                                calle, numero_exterior, acerca_de, latitud=0,
                                longitud=0):
    institucion = InstitucionEducativa.objects.create(
        encargado=encargado,
        nombre_institucion=nombre_institucion,
        latitud=latitud,
        longitud=longitud,
        codigo_postal=codigo_postal,
        municipio=municipio,
        colonia=colonia,
        calle=calle,
        numero_exterior=numero_exterior,
        acerca_de=acerca_de
    )

    for especialidad in especialidades:
        institucion.especialidades.add(especialidad)

    for miembro in miembros:
        institucion.miembros.add(miembro)

    return institucion
