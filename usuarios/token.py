from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class Token(PasswordResetTokenGenerator):

    # Usa el tiempo actual para generar el token (timestamp)
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        ) + six.text_type(user.is_active)


token_activacion = Token()
