import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 6:
            raise ValidationError(_("La contraseña debe tener al menos 6 caracteres."))
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("La contraseña debe contener al menos una letra mayúscula."))
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_("La contraseña debe contener al menos un carácter especial."))

    def get_help_text(self):
        return _(
            "Tu contraseña debe tener al menos 6 caracteres, incluir una mayúscula y un carácter especial."
        )
