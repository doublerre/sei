from usuarios.models import User, TipoUsuario


def crear_tipo_usuario(tipo):
    tipo_investigador = TipoUsuario.objects.create(
        tipo=tipo)

    return tipo_investigador


def crear_usuario(usuario, correo, contra, tipo=None, aprobado=False,
                  superusuario=False, staff=False):
    usuario = User.objects.create(
        username=usuario,
        email=correo,
        is_active=True,
        tipo_usuario=tipo,
        aprobado=aprobado,
        is_superuser=superusuario,
        is_staff=staff
        )
    usuario.set_password(contra)
    usuario.save()
    return usuario
