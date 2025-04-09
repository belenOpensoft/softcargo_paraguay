from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def email_o_si(value):
    if value != 'S/I' and value != '' and value is not None:
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError("Debe ser un email válido o 'S/I'")