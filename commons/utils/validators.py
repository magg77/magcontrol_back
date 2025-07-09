from django.core.exceptions import ValidationError

def validate_user_company(user_instance):
    """
    Valida que un usuario no superusuario tenga asociada una empresa.
    """
    if not user_instance.is_superuser and not user_instance.company:
        raise ValidationError("Solo el superusuario puede no tener empresa.")