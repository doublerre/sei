def user_is_staff_member(user):
    return user.is_staff

def user_is_other_role(user):
    return user.is_staff

def user_is_visitant(user):
    return user.tipo_usuario is None
