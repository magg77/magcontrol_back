# Funciones utilitarias generales
# validators.py, date_helpers.py, etc.

def capitalize_words(value):
    return ' '.join(word.capitalize() for word in value.split())
