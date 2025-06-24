from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def email_o_si(value):
    if value.strip().upper() == "S/I":
        return

    emails = [e.strip() for e in value.replace(';', ',').split(',') if e.strip()]

    for email in emails:
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Debe ser un email válido o 'S/I'")

