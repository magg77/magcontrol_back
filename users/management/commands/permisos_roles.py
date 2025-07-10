from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

# Formato 'app_label.ModelName': ['add_modelname', 'view_modelname']
ROLES_PERMISOS = {
    'Administradores': {
        'users.User': ['add_user', 'change_user', 'delete_user', 'view_user'],
        'companies.Company': ['add_company', 'change_company', 'delete_company', 'view_company'],
        'products.Product': ['add_product', 'change_product', 'view_product'],
        'products.Category': ['view_category'],
    },
    'Cajeros': {
        'users.User': ['view_user'],
        'companies.Company': ['view_company'],
        'products.Product': ['view_product'],
    },
    'Clientes': {},
    'Proveedores': {},
}

class Command(BaseCommand):
    help = 'Crea o actualiza los grupos de roles y sus permisos'

    def handle(self, *args, **options):
        for nombre_rol, permisos_por_modelo in ROLES_PERMISOS.items():
            grupo, creado = Group.objects.get_or_create(name=nombre_rol)
            permisos = []

            for ruta_modelo, codenames in permisos_por_modelo.items():
                app_label, model_name = ruta_modelo.lower().split('.')
                try:
                    ct = ContentType.objects.get(app_label=app_label, model=model_name)
                    perms = Permission.objects.filter(content_type=ct, codename__in=codenames)
                    permisos.extend(perms)
                except ContentType.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"[IGNORADO] Modelo {ruta_modelo} no encontrado. Verifica si existe y tiene migraciones aplicadas."
                    ))

            grupo.permissions.set(permisos)
            self.stdout.write(self.style.SUCCESS(
                f"{'Creado' if creado else 'Actualizado'} grupo: {nombre_rol} con permisos: {[p.codename for p in permisos]}"
            ))
